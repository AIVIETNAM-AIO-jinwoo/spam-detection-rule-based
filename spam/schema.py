"""Hợp đồng dữ liệu dùng chung cho mọi bước và mọi baseline.

KHÔNG đổi file này khi chưa thống nhất cả team: mọi module phụ thuộc vào nó.
"""
from dataclasses import dataclass, field

SPAM = "spam"
HAM = "ham"
LABELS = (HAM, SPAM)
POSITIVE = SPAM  # lớp dương khi tính precision / recall / F1


@dataclass(frozen=True)
class Message:
    label: str  # "spam" hoặc "ham"
    text: str


@dataclass
class Prediction:
    label: str                      # "spam" hoặc "ham"
    score: float = 0.0              # điểm spam, càng cao càng giống spam
    reasons: list = field(default_factory=list)  # lý do, ví dụ ["keyword:free", "has_url"]
