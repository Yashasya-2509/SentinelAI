"""FastAPI backend. Run: uvicorn sentinelai.api:app --reload"""
from __future__ import annotations

import io
import os
from functools import lru_cache
from typing import Optional

import pandas as pd
from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel, Field

from . import __version__
from .graph_analysis import summarize
from .inference import SentinelModel
from .investigation import DISPOSITIONS, connect, list_feedback, record_feedback

app = FastAPI(title="SentinelAI", version=__version__,
              description="Defensive network-flow threat detection and investigation API.")


class FlowRecord(BaseModel):
    src_ip: str
    dst_ip: str
    timestamp: str
    protocol: str
    duration: float = Field(ge=0)
    src_bytes: float = Field(ge=0)
    dst_bytes: float = Field(ge=0)
    src_pkts: float = Field(ge=0)
    dst_pkts: float = Field(ge=0)
    flow_rate: float = Field(ge=0)
    syn_count: float = Field(ge=0)


class Feedback(BaseModel):
    flow: dict
    disposition: str
    note: Optional[str] = ""


def _artifacts_dir() -> str:
    return os.environ.get("SENTINELAI_ARTIFACTS", "artifacts")


@lru_cache(maxsize=4)
def _load(path: str) -> SentinelModel:
    return SentinelModel.load(path)


def get_model() -> SentinelModel:
    try:
        return _load(_artifacts_dir())
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc))


async def _read_csv(file: UploadFile) -> pd.DataFrame:
    try:
        return pd.read_csv(io.BytesIO(await file.read()))
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=f"Could not parse CSV: {exc}")


@app.get("/health")
def health():
    return {"status": "ok", "version": __version__}


@app.get("/model")
def model_info():
    m = get_model()
    return {k: m.metadata[k] for k in ("model_version", "dataset_sha256", "classes", "features")}


@app.post("/predict")
def predict(records: list[FlowRecord]):
    if not records:
        raise HTTPException(status_code=400, detail="No records supplied.")
    df = pd.DataFrame([r.model_dump() for r in records])
    return get_model().predict(df).to_dict(orient="records")


@app.post("/predict/csv")
async def predict_csv(file: UploadFile = File(...)):
    df = await _read_csv(file)
    try:
        return get_model().predict(df).to_dict(orient="records")
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))


@app.post("/graph/summary")
async def graph_summary(file: UploadFile = File(...)):
    df = await _read_csv(file)
    try:
        preds = get_model().predict(df)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    return summarize(preds)


@app.post("/feedback")
def post_feedback(item: Feedback):
    if item.disposition not in DISPOSITIONS:
        raise HTTPException(status_code=422, detail=f"disposition must be one of {sorted(DISPOSITIONS)}")
    conn = connect(os.path.join(_artifacts_dir(), "cases.db"))
    return {"id": record_feedback(conn, item.flow, item.disposition, item.note or "")}


@app.get("/feedback")
def get_feedback():
    return list_feedback(connect(os.path.join(_artifacts_dir(), "cases.db")))
