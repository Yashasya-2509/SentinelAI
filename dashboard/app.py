"""Streamlit analyst dashboard. Run: streamlit run dashboard/app.py"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

import pandas as pd  # noqa: E402
import streamlit as st  # noqa: E402

from sentinelai.data import data_quality_report, generate_synthetic  # noqa: E402
from sentinelai.graph_analysis import endpoint_table, summarize  # noqa: E402
from sentinelai.inference import SentinelModel  # noqa: E402

st.set_page_config(page_title="SentinelAI", page_icon="🛡️", layout="wide")
st.title("🛡️ SentinelAI — Threat Detection & Investigation")
st.caption("Defensive analysis of authorized network-flow data. Predictions are decision support, not proof.")

artifacts = st.sidebar.text_input("Artifacts directory", str(ROOT / "artifacts"))
source = st.sidebar.radio("Data source", ["Upload CSV", "Synthetic demo data"])

try:
    model = SentinelModel.load(artifacts)
except FileNotFoundError as exc:
    st.error(f"{exc}")
    st.stop()

if source == "Upload CSV":
    up = st.sidebar.file_uploader("Network-flow CSV", type="csv")
    if up is None:
        st.info("Upload a CSV with the required columns, or choose synthetic demo data.")
        st.stop()
    raw = pd.read_csv(up)
else:
    raw = generate_synthetic(n=3000, seed=7)

try:
    preds = model.predict(raw)
except ValueError as exc:
    st.error(str(exc))
    st.stop()

tab_forensics, tab_threats, tab_anomaly, tab_graph, tab_model = st.tabs(
    ["Dataset forensics", "Threat detection", "Anomaly analysis", "Graph explorer", "Model & metrics"])

with tab_forensics:
    st.json(data_quality_report(raw))

with tab_threats:
    c1, c2, c3 = st.columns(3)
    c1.metric("Flows", len(preds))
    c2.metric("Needs review", int(preds["needs_review"].sum()))
    c3.metric("Signal disagreements", int(preds["review_reason"].str.contains("disagree").sum()))
    labels = sorted(preds["prediction"].unique())
    chosen = st.multiselect("Prediction", labels, default=labels)
    only_review = st.checkbox("Only flows needing review", value=True)
    view = preds[preds["prediction"].isin(chosen)]
    if only_review:
        view = view[view["needs_review"]]
    st.dataframe(view, use_container_width=True)
    st.download_button("Download results (CSV)", view.to_csv(index=False), "sentinelai_results.csv", "text/csv")

with tab_anomaly:
    st.write(f"Review threshold: **{model.detector.threshold_:.4f}**")
    counts, edges = pd.Series(preds["anomaly_score"]).pipe(lambda s: __import__("numpy").histogram(s, bins=30))
    st.bar_chart(pd.DataFrame({"flows": counts}, index=[round(e, 3) for e in edges[:-1]]))
    st.caption("An unusual flow is not automatically an attack.")

with tab_graph:
    st.json(summarize(preds))
    st.dataframe(endpoint_table(preds), use_container_width=True)

with tab_model:
    st.subheader("Global feature importance")
    st.bar_chart(model.global_importance().set_index("feature"))
    metrics_path = Path(artifacts) / "metrics.json"
    if metrics_path.exists():
        m = json.loads(metrics_path.read_text())
        st.metric("Macro-F1 (temporal test set)", f"{m['macro_f1']:.3f}")
        st.metric("Benign false-positive rate", f"{m['benign_false_positive_rate']:.3%}")
        st.write("Release gate:", "✅ passed" if m["release_gate"]["passed"] else "❌ failed")
        st.json(m)
