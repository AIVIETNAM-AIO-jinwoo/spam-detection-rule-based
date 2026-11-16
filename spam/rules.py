"""Bước 3 – Thống kê và luật (phụ trách: Duy Dương).

Hợp đồng:
  word_frequencies(messages, preprocess_fn) -> {"spam": Counter, "ham": Counter}
  RuleScorer.score(raw_text, tokens) -> (score: float, reasons: list[str])
"""
import re
from collections import Counter

from spam.schema import HAM, SPAM

URL_RE = re.compile(r"(https?://|www\.|\.com\b|\.co\.uk\b)", re.IGNORECASE)
PHONE_RE = re.compile(r"\b\d{5,}\b")


def word_frequencies(messages, preprocess_fn) -> dict:
    """Đếm tần suất từ theo từng nhãn – nguồn để chọn từ khóa cho luật."""
    freq = {SPAM: Counter(), HAM: Counter()}
    for m in messages:
        freq[m.label].update(preprocess_fn(m.text))
    return freq


# TODO(Duy Dương): thay danh sách này bằng từ khóa rút ra từ word_frequencies trên tập train
DEFAULT_KEYWORDS = {"free": 1.0, "win": 1.0, "winner": 1.5, "prize": 1.5, "claim": 1.5,
                    "urgent": 1.0, "cash": 1.0, "txt": 1.0, "call": 0.5, "£": 1.0}


class RuleScorer:
    def __init__(self, keywords=None, url_weight=1.5, phone_weight=1.5, caps_weight=1.0):
        self.keywords = dict(DEFAULT_KEYWORDS if keywords is None else keywords)
        self.url_weight = url_weight
        self.phone_weight = phone_weight
        self.caps_weight = caps_weight

    def score(self, raw_text: str, tokens: list):
        score, reasons = 0.0, []
        for tok in sorted(set(tokens)):
            if tok in self.keywords:
                score += self.keywords[tok]
                reasons.append(f"keyword:{tok}")
        if URL_RE.search(raw_text):
            score += self.url_weight
            reasons.append("has_url")
        if PHONE_RE.search(raw_text):
            score += self.phone_weight
            reasons.append("has_phone")
        letters = [c for c in raw_text if c.isalpha()]
        if len(letters) >= 10 and sum(c.isupper() for c in letters) / len(letters) > 0.5:
            score += self.caps_weight
            reasons.append("mostly_caps")
        return score, reasons
