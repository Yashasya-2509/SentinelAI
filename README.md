# SentinelAI

Defensive network-flow threat detection and investigation: supervised classifier + Isolation Forest anomaly
signal + leakage guard + NetworkX endpoint analysis + FastAPI + Streamlit + SQLite analyst feedback.

> Status: Stage 1–3 baseline. SHAP, GNN, autoencoder, drift monitor, MLflow and authentication are **planned**,
> not implemented. The bundled data is **synthetic** and only proves the pipeline runs; results on it say
> nothing about real-world detection quality.

## Quick start (macOS / Linux)
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
python scripts/generate_demo_data.py --rows 6000
python scripts/train_model.py
pytest -q
uvicorn sentinelai.api:app --reload --app-dir backend   # http://127.0.0.1:8000/docs
streamlit run dashboard/app.py
```
Windows: activate with `.venv\Scripts\activate`.

## In VS Code
Open the folder (or `SentinelAI.code-workspace`), accept the recommended extensions, select the `.venv`
interpreter, then use **Terminal → Run Task** (setup, train, tests, API, dashboard) or **Run and Debug**.

## Required CSV columns
`src_ip, dst_ip, timestamp, protocol, duration, src_bytes, dst_bytes, src_pkts, dst_pkts, flow_rate, syn_count`
(+ `label` for training). `src_ip/dst_ip/timestamp` are investigation metadata, never model inputs.

## API
`GET /health`, `GET /model`, `POST /predict` (JSON), `POST /predict/csv`, `POST /graph/summary`,
`POST /feedback`, `GET /feedback`.

## Design notes
- Temporal train/test split (no random shuffling of correlated flows).
- Anomaly detector trained on benign training flows only; threshold = percentile of benign scores.
- A benign prediction with an unusual anomaly score is flagged for review (signal disagreement).
- Release gate (macro-F1 and benign FPR thresholds in `configs/thresholds.yaml`).
- Next: Stage 2 — swap in CSE-CIC-IDS2018 (map columns to the schema in `data.py`).
