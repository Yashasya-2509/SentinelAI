import pandas as pd
import pytest

from sentinelai.data import data_quality_report, generate_synthetic, validate_schema


def test_synthetic_shape_and_labels():
    df = generate_synthetic(500, seed=1)
    assert len(df) == 500
    assert {"benign"} <= set(df["label"])


def test_validate_schema_rejects_missing_columns():
    with pytest.raises(ValueError):
        validate_schema(pd.DataFrame({"protocol": ["tcp"]}))


def test_quality_report_flags_leaky_column():
    df = generate_synthetic(600, seed=2)
    df["syn_count"] = df["label"].map({"benign": 0, "dos": 100, "portscan": 200, "bruteforce": 300})  # deliberately leaky
    report = data_quality_report(df)
    assert any(r.get("column") == "syn_count" for r in report["risks"])
