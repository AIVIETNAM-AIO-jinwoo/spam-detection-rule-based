"""Bảng so sánh mọi kết quả trên cùng một split, xếp theo F1. Dùng trong buổi demo thứ 2.

  python scripts/compare_results.py --split dev
"""
import argparse
import json

import _bootstrap  # noqa: F401
from spam.data import ROOT

parser = argparse.ArgumentParser()
parser.add_argument("--split", default="sample")
args = parser.parse_args()

rows = []
for path in sorted((ROOT / "results").glob(f"*__{args.split}.json")):
    data = json.loads(path.read_text(encoding="utf-8"))
    rows.append((data["name"], data["metrics"]))
if not rows:
    raise SystemExit(f"Chưa có kết quả nào cho split '{args.split}'. Chạy scripts/evaluate.py trước.")

rows.sort(key=lambda r: r[1]["f1"], reverse=True)
print(f"{'Tên':16s} {'Precision':>9s} {'Recall':>7s} {'F1':>6s} {'FP':>4s} {'FN':>4s}")
for name, m in rows:
    print(f"{name:16s} {m['precision']:9.3f} {m['recall']:7.3f} {m['f1']:6.3f} {m['fp']:4d} {m['fn']:4d}")
