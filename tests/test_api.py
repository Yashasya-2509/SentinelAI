import io

import pytest
from fastapi.testclient import TestClient

from sentinelai.data import generate_synthetic
from sentinelai.train import train


@pytest.fixture(scope="module")
def client(tmp_path_factory):
    d = tmp_path_factory.mktemp("api_art")
    train(generate_synthetic(3000, seed=8), d)
    import os
    os.environ["SENTINELAI_ARTIFACTS"] = str(d)
    from sentinelai.api import app
    return TestClient(app)


def test_health(client):
    assert client.get("/health").json()["status"] == "ok"


def test_predict_csv_and_graph(client):
    csv = generate_synthetic(100, seed=9).drop(columns=["label"]).to_csv(index=False)
    r = client.post("/predict/csv", files={"file": ("f.csv", io.BytesIO(csv.encode()), "text/csv")})
    assert r.status_code == 200 and len(r.json()) == 100
    g = client.post("/graph/summary", files={"file": ("f.csv", io.BytesIO(csv.encode()), "text/csv")})
    assert g.status_code == 200 and g.json()["nodes"] > 0


def test_predict_json_validation(client):
    assert client.post("/predict", json=[{"src_ip": "a"}]).status_code == 422


def test_feedback_roundtrip(client):
    r = client.post("/feedback", json={"flow": {"src_ip": "a", "model_version": "t"}, "disposition": "benign"})
    assert r.status_code == 200
    assert client.post("/feedback", json={"flow": {}, "disposition": "bogus"}).status_code == 422
