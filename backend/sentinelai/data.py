"""Data ingestion, synthetic data generation and dataset forensics (leakage guard)."""
from __future__ import annotations

import hashlib

import numpy as np
import pandas as pd
from sklearn.metrics import balanced_accuracy_score
from sklearn.tree import DecisionTreeClassifier

NUMERIC_FEATURES = ["duration", "src_bytes", "dst_bytes", "src_pkts", "dst_pkts", "flow_rate", "syn_count"]
CATEGORICAL_FEATURES = ["protocol"]
FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES
METADATA = ["src_ip", "dst_ip", "timestamp"]  # investigation context, never model inputs
LABEL = "label"
REQUIRED_COLUMNS = FEATURES + METADATA


def validate_schema(df: pd.DataFrame, require_label: bool = False) -> None:
    """Raise ValueError if required columns are missing."""
    needed = REQUIRED_COLUMNS + ([LABEL] if require_label else [])
    missing = [c for c in needed if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def load_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    validate_schema(df)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    return df


def dataset_checksum(df: pd.DataFrame) -> str:
    return hashlib.sha256(df.to_csv(index=False).encode("utf-8")).hexdigest()


# ----------------------------------------------------------------------------------------
# Synthetic data (Stage 1 only: proves the pipeline runs; NOT a substitute for real data)
# ----------------------------------------------------------------------------------------
def generate_synthetic(n: int = 6000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    classes = ["benign", "dos", "portscan", "bruteforce"]
    labels = rng.choice(classes, size=n, p=[0.80, 0.08, 0.07, 0.05])
    start = pd.Timestamp("2026-01-01")
    ts = start + pd.to_timedelta(np.sort(rng.uniform(0, 7 * 24 * 3600, n)), unit="s")

    internal = [f"10.0.0.{i}" for i in range(2, 60)]
    servers = [f"10.0.1.{i}" for i in range(2, 8)]
    attackers = [f"203.0.113.{i}" for i in range(10, 14)]

    rows = []
    for lab, t in zip(labels, ts):
        if lab == "benign":
            src, dst = rng.choice(internal), rng.choice(servers)
            proto = rng.choice(["tcp", "udp", "icmp"], p=[0.7, 0.25, 0.05])
            dur = rng.lognormal(1.0, 1.0)
            sb, db = rng.lognormal(7, 1.5), rng.lognormal(8, 1.5)
            sp, dp = rng.poisson(12) + 1, rng.poisson(14) + 1
            syn = rng.poisson(1)
        elif lab == "dos":
            src, dst = rng.choice(attackers), rng.choice(servers[:2])
            proto = rng.choice(["tcp", "udp"], p=[0.6, 0.4])
            dur = rng.lognormal(-1.0, 0.8)
            sb, db = rng.lognormal(8.5, 1.2), rng.lognormal(3, 1.0)
            sp, dp = rng.poisson(300) + 1, rng.poisson(3) + 1
            syn = rng.poisson(40)
        elif lab == "portscan":
            src, dst = rng.choice(attackers), rng.choice(servers + internal[:10])
            proto = "tcp"
            dur = rng.lognormal(-2.0, 0.7)
            sb, db = rng.lognormal(4, 0.6), rng.lognormal(3, 0.6)
            sp, dp = rng.poisson(2) + 1, rng.poisson(1) + 1
            syn = rng.poisson(3) + 1
        else:  # bruteforce
            src, dst = rng.choice(attackers), servers[2]
            proto = "tcp"
            dur = rng.lognormal(0.5, 0.5)
            sb, db = rng.lognormal(6, 0.7), rng.lognormal(6, 0.7)
            sp, dp = rng.poisson(8) + 1, rng.poisson(8) + 1
            syn = rng.poisson(2) + 1
        rows.append((src, dst, t, proto, dur, sb, db, sp, dp, syn, lab))

    df = pd.DataFrame(rows, columns=["src_ip", "dst_ip", "timestamp", "protocol", "duration",
                                     "src_bytes", "dst_bytes", "src_pkts", "dst_pkts", "syn_count", LABEL])
    df["flow_rate"] = (df["src_pkts"] + df["dst_pkts"]) / df["duration"].clip(lower=1e-3)
    # Overlap: a few benign flows look like heavy transfers so the task is not trivial.
    heavy = rng.random(n) < 0.02
    df.loc[heavy & (df[LABEL] == "benign"), "src_bytes"] *= 30
    return df[REQUIRED_COLUMNS + [LABEL]]


# ----------------------------------------------------------------------------------------
# Dataset forensics
# ----------------------------------------------------------------------------------------
def data_quality_report(df: pd.DataFrame, leakage_threshold: float = 0.99) -> dict:
    """Return a data-quality and leakage-risk report. Heuristics only: review findings manually."""
    report: dict = {"rows": int(len(df)), "columns": list(df.columns)}
    report["missing_values"] = {c: int(v) for c, v in df.isna().sum().items() if v > 0}
    report["duplicate_rows"] = int(df.duplicated().sum())
    report["constant_columns"] = [c for c in df.columns if df[c].nunique(dropna=False) <= 1]

    risks: list[dict] = []
    if LABEL in df.columns:
        counts = df[LABEL].value_counts()
        report["class_distribution"] = {k: int(v) for k, v in counts.items()}
        report["imbalance_ratio"] = float(counts.max() / max(counts.min(), 1))
        if report["imbalance_ratio"] > 10:
            risks.append({"type": "class_imbalance", "detail": "Do not rely on accuracy; use macro-F1 / PR-AUC."})

        # Single-feature near-perfect predictors often indicate label leakage.
        y = df[LABEL]
        for col in NUMERIC_FEATURES:
            if col in df.columns and df[col].notna().all():
                tree = DecisionTreeClassifier(max_depth=3, class_weight="balanced", random_state=0)
                tree.fit(df[[col]], y)
                score = balanced_accuracy_score(y, tree.predict(df[[col]]))
                if score >= leakage_threshold:
                    risks.append({"type": "possible_label_leakage", "column": col,
                                  "balanced_accuracy_single_feature": round(float(score), 4)})

    for col in [c for c in df.columns if pd.api.types.is_string_dtype(df[c]) or df[c].dtype == object]:
        if col != LABEL and df[col].nunique() / max(len(df), 1) > 0.95:
            risks.append({"type": "identifier_like_column", "column": col})
    if report["duplicate_rows"]:
        risks.append({"type": "duplicates", "detail": "Duplicates can leak between train and test splits."})
    report["risks"] = risks
    return report
