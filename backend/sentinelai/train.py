"""Training pipeline: temporal split, Random Forest classifier, Isolation Forest, metrics, artifacts."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, f1_score
from sklearn.pipeline import Pipeline

from .anomaly_detection import AnomalyDetector
from .config import load_experiment, load_thresholds
from .data import FEATURES, LABEL, dataset_checksum, data_quality_report, validate_schema
from .preprocessing import build_preprocessor


def temporal_split(df: pd.DataFrame, test_size: float):
    """Train on the earliest flows, test on the latest: avoids leakage from correlated neighbours."""
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)
    cut = int(len(df) * (1 - test_size))
    return df.iloc[:cut], df.iloc[cut:]


def evaluate(clf, detector, test_df: pd.DataFrame) -> dict:
    X, y = test_df[FEATURES], test_df[LABEL]
    pred = clf.predict(X)
    labels = sorted(y.unique())
    benign = y == "benign"
    fpr = float((pred[benign] != "benign").mean()) if benign.any() else float("nan")
    flags = detector.flag(X)
    return {
        "macro_f1": float(f1_score(y, pred, average="macro")),
        "benign_false_positive_rate": fpr,
        "per_class": classification_report(y, pred, output_dict=True, zero_division=0),
        "confusion_matrix": {"labels": labels, "matrix": confusion_matrix(y, pred, labels=labels).tolist()},
        "anomaly": {
            "threshold": detector.threshold_,
            "flag_rate_on_benign": float(flags[benign.values].mean()) if benign.any() else None,
            "flag_rate_on_attacks": float(flags[~benign.values].mean()) if (~benign).any() else None,
        },
    }


def release_gate(metrics: dict, thresholds: dict) -> dict:
    gate = thresholds["release_gate"]
    checks = {
        "macro_f1": metrics["macro_f1"] >= gate["min_macro_f1"],
        "benign_fpr": metrics["benign_false_positive_rate"] <= gate["max_benign_fpr"],
    }
    return {"passed": all(checks.values()), "checks": checks, "thresholds": gate}


def train(df: pd.DataFrame, out_dir: str | Path, experiment: dict | None = None,
          thresholds: dict | None = None) -> dict:
    exp = experiment or load_experiment()
    thr = thresholds or load_thresholds()
    validate_schema(df, require_label=True)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    train_df, test_df = temporal_split(df, exp["test_size"])

    clf = Pipeline([
        ("prep", build_preprocessor()),
        ("model", RandomForestClassifier(n_estimators=exp["n_estimators"], class_weight="balanced",
                                         random_state=exp["seed"], n_jobs=-1)),
    ]).fit(train_df[FEATURES], train_df[LABEL])

    detector = AnomalyDetector(percentile=thr["anomaly_percentile"], seed=exp["seed"]).fit(
        train_df.loc[train_df[LABEL] == "benign", FEATURES])

    metrics = evaluate(clf, detector, test_df)
    metrics["release_gate"] = release_gate(metrics, thr)

    version = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    metadata = {
        "model_version": version,
        "dataset_sha256": dataset_checksum(df),
        "rows_train": int(len(train_df)), "rows_test": int(len(test_df)),
        "features": FEATURES, "classes": list(clf.classes_),
        "sklearn_version": sklearn.__version__, "numpy_version": np.__version__,
        "experiment": exp, "thresholds": thr,
        "data_quality": data_quality_report(df),
    }
    joblib.dump(clf, out / "classifier.joblib")
    joblib.dump(detector, out / "anomaly.joblib")
    (out / "metrics.json").write_text(json.dumps(metrics, indent=2))
    (out / "metadata.json").write_text(json.dumps(metadata, indent=2, default=str))
    return {"metrics": metrics, "metadata": metadata}
