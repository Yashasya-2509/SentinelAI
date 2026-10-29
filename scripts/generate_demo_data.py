"""Generate synthetic network-flow data: python scripts/generate_demo_data.py --rows 6000"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from sentinelai.data import generate_synthetic  # noqa: E402

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", type=int, default=6000)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", default="data/sample/synthetic_flows.csv")
    a = ap.parse_args()
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    generate_synthetic(a.rows, a.seed).to_csv(out, index=False)
    print(f"Wrote {a.rows} rows to {out}")
