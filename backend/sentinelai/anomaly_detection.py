"""Isolation Forest anomaly detector trained on benign traffic only."""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.pipeline import Pipeline

from .preprocessing import build_preprocessor


class AnomalyDetector:
    """Higher score = more unusual. An unusual flow is NOT automatically an attack."""

    def __init__(self, percentile: float = 97.0, n_estimators: int = 200, seed: int = 42):
        self.percentile = percentile
        self.pipeline = Pipeline([
            ("prep", build_preprocessor()),
            ("iso", IsolationForest(n_estimators=n_estimators, random_state=seed, n_jobs=-1)),
        ])
        self.threshold_: float | None = None

    def fit(self, X_benign: pd.DataFrame) -> "AnomalyDetector":
        self.pipeline.fit(X_benign)
        scores = self.score(X_benign)
        self.threshold_ = float(np.percentile(scores, self.percentile))
        return self

    def score(self, X: pd.DataFrame) -> np.ndarray:
        return -self.pipeline.score_samples(X)

    def flag(self, X: pd.DataFrame) -> np.ndarray:
        if self.threshold_ is None:
            raise RuntimeError("Detector is not fitted.")
        return self.score(X) > self.threshold_
