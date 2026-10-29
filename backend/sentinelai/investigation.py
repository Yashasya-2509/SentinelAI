"""Minimal SQLite case store for analyst dispositions (human-in-the-loop feedback)."""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DISPOSITIONS = {"confirmed_attack", "benign", "uncertain", "needs_review"}

_SCHEMA = """
CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL,
    model_version TEXT NOT NULL,
    src_ip TEXT, dst_ip TEXT, flow_timestamp TEXT,
    prediction TEXT, anomaly_score REAL,
    disposition TEXT NOT NULL,
    note TEXT
)"""


def connect(db_path: str | Path = "artifacts/cases.db") -> sqlite3.Connection:
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.execute(_SCHEMA)
    return conn


def record_feedback(conn: sqlite3.Connection, flow: dict, disposition: str, note: str = "") -> int:
    if disposition not in DISPOSITIONS:
        raise ValueError(f"disposition must be one of {sorted(DISPOSITIONS)}")
    cur = conn.execute(
        "INSERT INTO feedback (created_at, model_version, src_ip, dst_ip, flow_timestamp, prediction,"
        " anomaly_score, disposition, note) VALUES (?,?,?,?,?,?,?,?,?)",
        (datetime.now(timezone.utc).isoformat(), flow.get("model_version", "unknown"), flow.get("src_ip"),
         flow.get("dst_ip"), str(flow.get("timestamp")), flow.get("prediction"),
         flow.get("anomaly_score"), disposition, note))
    conn.commit()
    return int(cur.lastrowid)


def list_feedback(conn: sqlite3.Connection) -> list[dict]:
    cur = conn.execute("SELECT * FROM feedback ORDER BY id DESC")
    cols = [c[0] for c in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]
