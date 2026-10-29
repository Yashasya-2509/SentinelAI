"""Print saved metrics; exit 1 if the release gate failed: python scripts/evaluate_model.py"""
import argparse
import json
import sys
from pathlib import Path

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--artifacts", default="artifacts")
    a = ap.parse_args()
    m = json.loads((Path(a.artifacts) / "metrics.json").read_text())
    print(json.dumps({k: m[k] for k in ("macro_f1", "benign_false_positive_rate", "anomaly", "release_gate")}, indent=2))
    sys.exit(0 if m["release_gate"]["passed"] else 1)
