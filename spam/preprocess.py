"""Bước 2 – Tiền xử lý (phụ trách: Thúy).

Hợp đồng: preprocess(text: str) -> list[str]
Bản dưới đây chỉ là phiên bản tối thiểu để pipeline chạy được từ ngày đầu.
"""
import re

# TODO(Thúy): mở rộng danh sách stopword, cân nhắc giữ lại số / ký hiệu tiền tệ vì là dấu hiệu spam
STOPWORDS = {"a", "an", "the", "is", "are", "to", "of", "and", "in", "on", "for", "you", "i", "it", "me", "my"}

_TOKEN_RE = re.compile(r"[a-z0-9£$€]+")


def normalize(text: str) -> str:
    """TODO(Thúy): thay link bằng <url>, số điện thoại bằng <phone>, chuẩn hóa khoảng trắng."""
    return text.lower()


def tokenize(text: str) -> list:
    return _TOKEN_RE.findall(text)


def remove_stopwords(tokens: list) -> list:
    return [t for t in tokens if t not in STOPWORDS]


def preprocess(text: str) -> list:
    return remove_stopwords(tokenize(normalize(text)))
