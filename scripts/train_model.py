"""Train and save artifacts: python scripts/train_model.py --data data/sample/synthetic_flows.csv"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from sentinelai.data import load_csv  # noqa: E402
from sentinelai.train import train  # noqa: E402

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/sample/synthetic_flows.csv")
    ap.add_argument("--out", default="artifacts")
    a = ap.parse_args()
    result = train(load_csv(a.data), a.out)
    m = result["metrics"]
    print(f"Model version : {result['metadata']['model_version']}")
    print(f"Macro-F1      : {m['macro_f1']:.4f}")
    print(f"Benign FPR    : {m['benign_false_positive_rate']:.4%}")
    print(f"Release gate  : {'PASSED' if m['release_gate']['passed'] else 'FAILED'}")
    risks = result["metadata"]["data_quality"]["risks"]
    print("Data risks    :", json.dumps(risks) if risks else "none detected")
    print(f"Artifacts in  : {a.out}/")
