import pandas as pd

from sentinelai.graph_analysis import endpoint_table, summarize


def _df():
    return pd.DataFrame({
        "src_ip": ["a", "a", "a", "b"], "dst_ip": ["x", "y", "z", "x"],
        "needs_review": [True, True, False, False],
    })


def test_summary_counts():
    s = summarize(_df())
    assert s["nodes"] == 5 and s["edges"] == 4


def test_endpoint_table_ranks_flagged_first():
    t = endpoint_table(_df())
    assert t.iloc[0]["flagged_flows"] >= t.iloc[-1]["flagged_flows"]
    assert set(t["endpoint"]) == {"a", "b", "x", "y", "z"}
