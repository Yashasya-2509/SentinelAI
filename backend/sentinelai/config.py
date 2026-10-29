"""Load YAML configuration with safe defaults."""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]

DEFAULT_EXPERIMENT = {
    "seed": 42,
    "test_size": 0.3,          # temporal split: last 30% of flows are the test set
    "n_estimators": 200,
}
DEFAULT_THRESHOLDS = {
    "anomaly_percentile": 97.0,  # percentile of benign training scores used as the threshold
    "min_confidence": 0.60,      # below this the classifier is considered uncertain
    "release_gate": {"min_macro_f1": 0.80, "max_benign_fpr": 0.05},
}


def _load(path: Path, defaults: dict) -> dict:
    cfg = dict(defaults)
    if path.exists():
        with open(path, "r", encoding="utf-8") as fh:
            cfg.update(yaml.safe_load(fh) or {})
    return cfg


def load_experiment(path: str | Path | None = None) -> dict:
    return _load(Path(path) if path else ROOT / "configs" / "experiment.yaml", DEFAULT_EXPERIMENT)


def load_thresholds(path: str | Path | None = None) -> dict:
    return _load(Path(path) if path else ROOT / "configs" / "thresholds.yaml", DEFAULT_THRESHOLDS)
