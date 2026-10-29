"""Load trained artifacts and enrich flows with prediction, confidence and anomaly signals."""
from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from .data import FEATURES, METADATA, validate_schema


class SentinelModel:
    def __init__(self, classifier, detector, metadata: dict):
        self.classifier = classifier
        self.detector = detector
        self.metadata = metadata
        self.min_confidence = metadata.get("thresholds", {}).get("min_confidence", 0.6)

    @classmethod
    def load(cls, artifacts_dir: str | Path) -> "SentinelModel":
        d = Path(artifacts_dir)
        if not (d / "classifier.joblib").exists():
            raise FileNotFoundError(f"No trained model in {d}. Run `python scripts/train_model.py` first.")
        return cls(joblib.load(d / "classifier.joblib"), joblib.load(d / "anomaly.joblib"),
                   json.loads((d / "metadata.json").read_text()))

    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        validate_schema(df)
        X = df[FEATURES]
        proba = self.classifier.predict_proba(X)
        classes = self.classifier.classes_
        pred = classes[proba.argmax(axis=1)]
        conf = proba.max(axis=1)
        score = self.detector.score(X)
        flag = score > self.detector.threshold_

        reasons = []
        for p, c, f in zip(pred, conf, flag):
            r = []
            if p != "benign":
                r.append(f"classifier predicts {p}")
            if p == "benign" and f:
                r.append("signals disagree: benign prediction but unusual traffic")
            if c < self.min_confidence:
                r.append("low classifier confidence")
            reasons.append("; ".join(r))

        out = df[[c for c in METADATA if c in df.columns]].copy()
        out["prediction"] = pred
        out["confidence"] = np.round(conf, 4)
        out["anomaly_score"] = np.round(score, 4)
        out["anomaly_flag"] = flag
        out["needs_review"] = [bool(r) for r in reasons]
        out["review_reason"] = reasons
        out["model_version"] = self.metadata["model_version"]
        for cls_name, col in zip(classes, proba.T):
            out[f"proba_{cls_name}"] = np.round(col, 4)
        return out.reset_index(drop=True)

    def global_importance(self) -> pd.DataFrame:
        """Global RandomForest feature importances (model behaviour, not proof of cause)."""
        prep = self.classifier.named_steps["prep"]
        names = [n.split("__", 1)[-1] for n in prep.get_feature_names_out()]
        imp = self.classifier.named_steps["model"].feature_importances_
        return pd.DataFrame({"feature": names, "importance": imp}).sort_values("importance", ascending=False)
