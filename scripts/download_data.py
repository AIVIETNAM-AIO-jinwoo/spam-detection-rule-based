"""Tải SMS Spam Collection (UCI) về data/raw/SMSSpamCollection và kiểm tra.

Nguồn DUY NHẤT của team: https://archive.ics.uci.edu/dataset/228/sms+spam+collection
Không dùng bản trên Kaggle hay nơi khác: định dạng và mã hóa có thể khác.

Chạy: python scripts/download_data.py
Không tải được (mạng chặn)? Bấm Download trên trang UCI ở trên, giải nén và đặt file
`SMSSpamCollection` vào data/raw/, rồi chạy lại script này để kiểm tra.
"""
import io
import urllib.request
import zipfile

import _bootstrap  # noqa: F401
from spam.data import RAW_FILE

DATASET_PAGE = "https://archive.ics.uci.edu/dataset/228/sms+spam+collection"
URLS = ["https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip"]
EXPECTED = {"total": 5574, "ham": 4827, "spam": 747}


def download() -> bool:
    for url in URLS:
        try:
            print(f"Đang tải {url} ...")
            with urllib.request.urlopen(url, timeout=60) as resp:
                data = resp.read()
            with zipfile.ZipFile(io.BytesIO(data)) as zf:
                name = next(n for n in zf.namelist() if n.endswith("SMSSpamCollection"))
                RAW_FILE.parent.mkdir(parents=True, exist_ok=True)
                RAW_FILE.write_bytes(zf.read(name))
            return True
        except Exception as exc:  # noqa: BLE001
            print(f"  Không được: {exc}")
    return False


def verify() -> None:
    counts = {"ham": 0, "spam": 0}
    with open(RAW_FILE, encoding="utf-8", errors="replace") as f:
        for line in f:
            label = line.split("\t", 1)[0]
            if label in counts:
                counts[label] += 1
    total = counts["ham"] + counts["spam"]
    print(f"Đọc được {total} tin: {counts['ham']} ham, {counts['spam']} spam")
    if (total, counts["ham"], counts["spam"]) != (EXPECTED["total"], EXPECTED["ham"], EXPECTED["spam"]):
        raise SystemExit(f"Số lượng không khớp bản gốc {EXPECTED}. Kiểm tra lại file.")
    print("Dữ liệu gốc khớp bản SMS Spam Collection v.1.")


if __name__ == "__main__":
    if not RAW_FILE.exists() and not download():
        raise SystemExit("Không tải được. Làm theo hướng dẫn tải tay ở đầu file này.")
    verify()
