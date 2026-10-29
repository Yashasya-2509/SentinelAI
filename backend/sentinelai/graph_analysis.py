"""Endpoint relationship analysis. Initial implementation uses NetworkX summaries (no GNN yet)."""
from __future__ import annotations

import networkx as nx
import pandas as pd


def build_graph(df: pd.DataFrame, flagged_col: str = "needs_review") -> nx.DiGraph:
    """Nodes = endpoints, directed edges = observed flows aggregated per (src, dst)."""
    g = nx.DiGraph()
    for (src, dst), grp in df.groupby(["src_ip", "dst_ip"]):
        g.add_edge(src, dst, flows=int(len(grp)),
                   flagged=int(grp[flagged_col].sum()) if flagged_col in grp else 0)
    return g


def endpoint_table(df: pd.DataFrame, flagged_col: str = "needs_review") -> pd.DataFrame:
    """Per-endpoint degree, flow volume and share of flagged flows, ranked by flagged flows."""
    g = build_graph(df, flagged_col)
    rows = []
    for node in g.nodes:
        out_e = g.out_edges(node, data=True)
        in_e = g.in_edges(node, data=True)
        flows_out = sum(d["flows"] for _, _, d in out_e)
        flows_in = sum(d["flows"] for _, _, d in in_e)
        flagged_out = sum(d["flagged"] for _, _, d in g.out_edges(node, data=True))
        flagged_in = sum(d["flagged"] for _, _, d in g.in_edges(node, data=True))
        total = flows_out + flows_in
        rows.append({
            "endpoint": node, "out_degree": g.out_degree(node), "in_degree": g.in_degree(node),
            "flows_out": flows_out, "flows_in": flows_in,
            "flagged_flows": flagged_out + flagged_in,
            "flagged_ratio": round((flagged_out + flagged_in) / total, 4) if total else 0.0,
        })
    cols = ["endpoint", "out_degree", "in_degree", "flows_out", "flows_in", "flagged_flows", "flagged_ratio"]
    return pd.DataFrame(rows, columns=cols).sort_values(["flagged_flows", "out_degree"], ascending=False).reset_index(drop=True)


def summarize(df: pd.DataFrame, top_k: int = 5, flagged_col: str = "needs_review") -> dict:
    g = build_graph(df, flagged_col)
    table = endpoint_table(df, flagged_col)
    return {
        "nodes": g.number_of_nodes(),
        "edges": g.number_of_edges(),
        "weakly_connected_components": nx.number_weakly_connected_components(g) if g.number_of_nodes() else 0,
        "top_sources_by_out_degree": table.nlargest(top_k, "out_degree")[["endpoint", "out_degree"]].to_dict("records"),
        "top_targets_by_in_degree": table.nlargest(top_k, "in_degree")[["endpoint", "in_degree"]].to_dict("records"),
        "top_endpoints_by_flagged_flows": table.head(top_k)[["endpoint", "flagged_flows", "flagged_ratio"]].to_dict("records"),
    }
