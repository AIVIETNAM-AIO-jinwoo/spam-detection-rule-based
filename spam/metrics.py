"""Bước 4 – Đánh giá (phụ trách: Ngọc). Đây là THƯỚC ĐO CHUNG của cả team.

Mọi baseline và pipeline chính đều được chấm bằng file này để so sánh công bằng.
Sprint 2, Ngọc mở rộng: quét ngưỡng, so với thư viện, phân tích lỗi.
"""
from spam.schema import POSITIVE


def confusion_matrix(y_true, y_pred, positive=POSITIVE) -> dict:
    if len(y_true) != len(y_pred):
        raise ValueError("y_true và y_pred phải dài bằng nhau")
    cm = {"tp": 0, "fp": 0, "fn": 0, "tn": 0}
    for t, p in zip(y_true, y_pred):
        if p == positive:
            cm["tp" if t == positive else "fp"] += 1
        else:
            cm["fn" if t == positive else "tn"] += 1
    return cm


def _div(a, b):
    return a / b if b else 0.0


def report(y_true, y_pred, positive=POSITIVE) -> dict:
    cm = confusion_matrix(y_true, y_pred, positive)
    precision = _div(cm["tp"], cm["tp"] + cm["fp"])
    recall = _div(cm["tp"], cm["tp"] + cm["fn"])
    return {
        **cm,
        "accuracy": _div(cm["tp"] + cm["tn"], len(y_true)),
        "precision": precision,
        "recall": recall,
        "f1": _div(2 * precision * recall, precision + recall),
    }


def format_report(r: dict, title: str = "") -> str:
    lines = [title] if title else []
    lines += [
        f"  Confusion matrix   TP={r['tp']}  FP={r['fp']}  FN={r['fn']}  TN={r['tn']}",
        f"  Accuracy  {r['accuracy']:.4f}",
        f"  Precision {r['precision']:.4f}   (trong số tin bị chặn, bao nhiêu là spam thật)",
        f"  Recall    {r['recall']:.4f}   (trong số spam thật, bắt được bao nhiêu)",
        f"  F1        {r['f1']:.4f}",
    ]
    return "\n".join(lines)
