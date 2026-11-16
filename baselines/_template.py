"""Baseline cá nhân – Sprint 1. Copy file này thành baselines/<ten-ban>.py rồi tự viết.

Luật chơi:
  - Một file duy nhất, chỉ dùng thư viện chuẩn của Python, khoảng 50 dòng.
  - Đi đủ 5 bước của pipeline, dù mỗi bước rất đơn giản.
  - Giữ đúng HỢP ĐỒNG bên dưới để scripts/evaluate.py chấm được.

Chạy thử:  python scripts/evaluate.py baselines/<ten-ban>.py --split sample
"""

NAME = "ten-ban"  # TODO: đổi thành tên bạn, viết thường không dấu, ví dụ "thuy"

SPAM, HAM = "spam", "ham"


# ---- Bước 2: tiền xử lý ---------------------------------------------------
def preprocess(text: str) -> list:
    """Trả về list từ. Gợi ý: chữ thường, tách theo khoảng trắng, bỏ dấu câu."""
    raise NotImplementedError


# ---- Bước 3: luật chấm điểm ------------------------------------------------
KEYWORDS = {}  # TODO: vài từ khóa spam và trọng số, ví dụ {"free": 1.0}


def score(text: str, tokens: list) -> float:
    """Trả về điểm spam. Gợi ý: cộng trọng số từ khóa, cộng điểm nếu có link."""
    raise NotImplementedError


# ---- Bước 5: dự đoán (HỢP ĐỒNG – bắt buộc) ---------------------------------
THRESHOLD = 1.0


def predict(text: str) -> str:
    """Trả về đúng chuỗi "spam" hoặc "ham"."""
    return SPAM if score(text, preprocess(text)) >= THRESHOLD else HAM


# ---- Bước 4: tự cài đặt metric (không bắt buộc, nhưng nên làm) -------------
def my_report(y_true: list, y_pred: list) -> dict:
    """Trả về dict có các khóa tp, fp, fn, tn, precision, recall, f1 (lớp dương là "spam").

    evaluate.py sẽ so kết quả của bạn với thước đo chung và báo khớp / lệch.
    """
    raise NotImplementedError
