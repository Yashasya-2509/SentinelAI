"""Feature preprocessing shared by the classifier and the anomaly detector."""
from __future__ import annotations

import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler

from .data import CATEGORICAL_FEATURES, NUMERIC_FEATURES


def _log1p_clip(x):
    """Network-flow counters are heavy-tailed and non-negative; log-scale them."""
    return np.log1p(np.clip(x, 0, None))


def build_preprocessor() -> ColumnTransformer:
    numeric = Pipeline([
        ("log", FunctionTransformer(_log1p_clip, feature_names_out="one-to-one")),
        ("scale", StandardScaler()),
    ])
    categorical = OneHotEncoder(handle_unknown="ignore")
    return ColumnTransformer([
        ("num", numeric, NUMERIC_FEATURES),
        ("cat", categorical, CATEGORICAL_FEATURES),
    ])
