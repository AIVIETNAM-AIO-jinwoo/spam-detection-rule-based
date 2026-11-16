"""Chấm một baseline hoặc pipeline chính bằng THƯỚC ĐO CHUNG (spam/metrics.py).

  python scripts/evaluate.py baselines/thuy.py --split sample
  python scripts/evaluate.py baselines/thuy.py --split dev
  python scripts/evaluate.py pipeline --split dev
  python scripts/evaluate.py pipeline --split test --final   # chỉ dùng ở cuối sprint 3

Kết quả lưu vào results/<tên>__<split>.json, kèm danh sách tin bị đoán sai để phân tích lỗi.
"""
import argparse
import importlib.util
import json
from datetime import datetime
from pathlib import Path

import _bootstrap  # noqa: F401
from spam.data import ROOT, load_split
from spam.metrics import format_report, report
from spam.pipeline import SpamPipeline
from spam.schema import LABELS

RESULTS_DIR = ROOT / "results"
CHECK_KEYS = ("tp", "fp", "fn", "tn", "precision", "recall", "f1")


def load_baseline(path):
    spec = importlib.util.spec_from_file_location(Path(path).stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for attr in ("NAME", "predict"):
        if not hasattr(module, attr):
            raise SystemExit(f"{path} thiếu `{attr}` (xem baselines/README.md)")
    return module


def compare_own_metrics(module, y_true, y_pred, ref) -> None:
    if not hasattr(module, "my_report"):
        print("\n(Chưa có my_report: hãy tự cài đặt metric để so với thước đo chung.)")
        return
    mine = module.my_report(y_true, y_pred)
    print("\nSo metric tự cài đặt với thước đo chung:")
    for key in CHECK_KEYS:
        same = key in mine and abs(float(mine[key]) - float(ref[key])) < 1e-9
        print(f"  {key:9s} {'khớp' if same else 'LỆCH'}   của bạn={mine.get(key)}  chung={ref[key]}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="đường dẫn baseline (.py) hoặc chữ 'pipeline'")
    parser.add_argument("--split", default="sample", choices=["sample", "train", "dev", "test"])
    parser.add_argument("--final", action="store_true", help="bắt buộc khi chấm trên tập test")
    args = parser.parse_args()
    if args.split == "test" and not args.final:
        raise SystemExit("Tập test chỉ dùng ở cuối sprint 3. Thêm --final nếu cả team đã đồng ý.")

    messages = load_split(args.split)
    y_true = [m.label for m in messages]
    module = None
    if args.target == "pipeline":
        name = "pipeline"
        y_pred = [p.label for p in SpamPipeline().predict_many(m.text for m in messages)]
    else:
        module = load_baseline(args.target)
        name = module.NAME
        y_pred = [module.predict(m.text) for m in messages]
    bad = sorted({p for p in y_pred if p not in LABELS})
    if bad:
        raise SystemExit(f"predict() trả về nhãn không hợp lệ {bad}; chỉ được dùng {LABELS}")

    ref = report(y_true, y_pred)
    print(format_report(ref, f"{name} trên {args.split} ({len(messages)} tin)"))
    if module is not None:
        compare_own_metrics(module, y_true, y_pred, ref)

    errors = [{"true": t, "pred": p, "text": m.text}
              for m, t, p in zip(messages, y_true, y_pred) if t != p]
    RESULTS_DIR.mkdir(exist_ok=True)
    out = RESULTS_DIR / f"{name}__{args.split}.json"
    out.write_text(json.dumps({"name": name, "split": args.split, "n": len(messages),
                               "time": datetime.now().isoformat(timespec="seconds"),
                               "metrics": ref, "errors": errors}, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8")
    print(f"\nĐã lưu {out.relative_to(ROOT)} ({len(errors)} tin đoán sai).")


if __name__ == "__main__":
    main()
