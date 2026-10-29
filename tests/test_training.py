import json

from sentinelai.data import generate_synthetic
from sentinelai.train import temporal_split, train


def test_temporal_split_has_no_overlap_in_time():
    df = generate_synthetic(400, seed=3)
    tr, te = temporal_split(df, 0.3)
    assert tr["timestamp"].max() <= te["timestamp"].min()


def test_training_writes_artifacts_and_reasonable_metrics(tmp_path):
    result = train(generate_synthetic(3000, seed=4), tmp_path)
    for name in ("classifier.joblib", "anomaly.joblib", "metrics.json", "metadata.json"):
        assert (tmp_path / name).exists()
    assert result["metrics"]["macro_f1"] > 0.7
    meta = json.loads((tmp_path / "metadata.json").read_text())
    assert len(meta["dataset_sha256"]) == 64
