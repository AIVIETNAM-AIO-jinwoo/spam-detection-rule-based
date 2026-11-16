"""Bước 1 – Dữ liệu (phụ trách: Tuấn Duy). Đọc / ghi file TSV: mỗi dòng `label<TAB>text`."""
from pathlib import Path

from spam.schema import LABELS, Message

ROOT = Path(__file__).resolve().parent.parent
SPLITS_DIR = ROOT / "data" / "splits"
RAW_FILE = ROOT / "data" / "raw" / "SMSSpamCollection"


def load_tsv(path) -> list:
    """Đọc file TSV thành list[Message]. Báo lỗi rõ ràng nếu nhãn sai định dạng."""
    messages = []
    with open(path, encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.rstrip("\n")
            if not line:
                continue
            label, sep, text = line.partition("\t")
            if not sep or label not in LABELS:
                raise ValueError(f"{path}:{line_no}: dòng không đúng định dạng 'label<TAB>text'")
            messages.append(Message(label=label, text=text))
    return messages


def save_tsv(messages, path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for m in messages:
            f.write(f"{m.label}\t{m.text}\n")


def load_split(name: str) -> list:
    """name: 'sample' | 'train' | 'dev' | 'test'."""
    path = SPLITS_DIR / f"{name}.tsv"
    if not path.exists():
        raise FileNotFoundError(f"Chưa có {path}. Chạy: python scripts/download_data.py && python scripts/make_splits.py")
    return load_tsv(path)
