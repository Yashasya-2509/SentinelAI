# SentinelAI Architecture (Stage 1–3 implemented)

CSV flows -> schema validation -> dataset forensics -> temporal split -> preprocessing
-> RandomForest classifier + IsolationForest (benign-only) -> enrichment (confidence, anomaly score,
signal-disagreement flag) -> NetworkX endpoint summaries -> FastAPI + Streamlit -> SQLite feedback.

Implemented: baseline classifier, anomaly scoring, leakage heuristics, release gate, graph summaries,
API, dashboard, feedback store, tests, CI.
Planned (not implemented): SHAP, gradient boosting, autoencoder, GNN, alert correlation/cases UI,
drift monitor, MLflow, authentication.
