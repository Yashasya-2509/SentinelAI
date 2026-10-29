import pytest

from sentinelai.data import generate_synthetic
from sentinelai.inference import SentinelModel
from sentinelai.train import train


@pytest.fixture(scope="module")
def model(tmp_path_factory):
    d = tmp_path_factory.mktemp("art")
    train(generate_synthetic(3000, seed=5), d)
    return SentinelModel.load(d)


def test_predict_columns(model):
    out = model.predict(generate_synthetic(50, seed=6))
    for col in ("prediction", "confidence", "anomaly_score", "anomaly_flag", "needs_review", "model_version"):
        assert col in out.columns
    assert out["confidence"].between(0, 1).all()


def test_missing_columns_rejected(model):
    with pytest.raises(ValueError):
        model.predict(generate_synthetic(10, seed=6).drop(columns=["protocol"]))


def test_global_importance(model):
    assert not model.global_importance().empty
