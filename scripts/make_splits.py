"""Tạo bộ chia dữ liệu trên máy của bạn và đối chiếu với cả team.

  python scripts/make_splits.py           # mọi người tự chạy trên máy mình
  python scripts/make_splits.py --check   # chỉ kiểm tra file đang có, không tạo lại

Bộ chia là tất định: cùng file gốc + cùng seed thì máy ai cũng ra đúng một kết quả.
Script in ra MÃ BỘ CHIA; cả team so mã này trong nhóm chat là biết dữ liệu đã giống nhau.
Người đầu tiên mở pull request commit file data/splits/manifest.json; từ đó script tự đối chiếu.

Quy tắc chia:
  - Bỏ tin trùng nội dung (giữ bản đầu); tin trùng mà khác nhãn thì bỏ hết.
  - Chia phân tầng theo nhãn: 70% train / 15% dev / 15% test, seed 42.
  - sample: 10 spam + 10 ham lấy từ train, dùng cho baseline sprint 1.
"""
import argparse
import hashlib
import json
import random

import _bootstrap  # noqa: F401
from spam.data import RAW_FILE, SPLITS_DIR, save_tsv
from spam.schema import HAM, LABELS, SPAM, Message

SEED = 42
RATIOS = {"train": 0.70, "dev": 0.15, "test": 0.15}
MANIFEST = SPLITS_DIR / "manifest.json"
SPLIT_NAMES = ("train", "dev", "test", "sample")


def sha256(path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_raw() -> list:
    rows = []
    with open(RAW_FILE, encoding="utf-8", errors="replace") as f:
        for line in f:
            label, sep, text = line.rstrip("\n").partition("\t")
            text = " ".join(text.split())
            if sep and label in LABELS and text:
                rows.append(Message(label, text))
    return rows


def deduplicate(rows):
    labels_by_text = {}
    for m in rows:
        labels_by_text.setdefault(m.text, set()).add(m.label)
    seen, kept, conflicts = set(), [], 0
    for m in rows:
        if len(labels_by_text[m.text]) > 1:
            conflicts += 1
            continue
        if m.text not in seen:
            seen.add(m.text)
            kept.append(m)
    return kept, len(rows) - len(kept), conflicts


def split(rows):
    rng = random.Random(SEED)
    parts = {name: [] for name in RATIOS}
    for label in (HAM, SPAM):
        group = [m for m in rows if m.label == label]
        rng.shuffle(group)
        n_train = round(len(group) * RATIOS["train"])
        n_dev = round(len(group) * RATIOS["dev"])
        parts["train"] += group[:n_train]
        parts["dev"] += group[n_train:n_train + n_dev]
        parts["test"] += group[n_train + n_dev:]
    for name in parts:
        rng.shuffle(parts[name])
    train = parts["train"]
    parts["sample"] = [m for m in train if m.label == SPAM][:10] + [m for m in train if m.label == HAM][:10]
    return parts


def fingerprint(manifest) -> str:
    joined = manifest["raw_sha256"] + "".join(manifest["splits"][n]["sha256"] for n in SPLIT_NAMES)
    return hashlib.sha256(joined.encode()).hexdigest()[:12]


def compare(manifest, shared) -> bool:
    ok = manifest["raw_sha256"] == shared.get("raw_sha256")
    print(f"  raw    {'OK' if ok else 'KHÁC BẢN CHUNG (tải lại từ trang UCI)'}")
    for name in SPLIT_NAMES:
        same = manifest["splits"][name]["sha256"] == shared["splits"].get(name, {}).get("sha256")
        ok &= same
        print(f"  {name:6s} {'OK' if same else 'KHÁC BẢN CHUNG'}")
    return ok


def make() -> None:
    if not RAW_FILE.exists():
        raise SystemExit("Chưa có dữ liệu gốc. Chạy: python scripts/download_data.py")
    rows = read_raw()
    kept, removed, conflicts = deduplicate(rows)
    print(f"Gốc: {len(rows)} tin. Bỏ {removed} tin trùng (trong đó {conflicts} tin trùng nhưng khác nhãn).")
    parts = split(kept)
    manifest = {"seed": SEED, "ratios": RATIOS,
                "source": "https://archive.ics.uci.edu/dataset/228/sms+spam+collection",
                "raw_sha256": sha256(RAW_FILE), "splits": {}}
    for name in SPLIT_NAMES:
        path = SPLITS_DIR / f"{name}.tsv"
        save_tsv(parts[name], path)
        n_spam = sum(m.label == SPAM for m in parts[name])
        manifest["splits"][name] = {"total": len(parts[name]), "spam": n_spam,
                                    "ham": len(parts[name]) - n_spam, "sha256": sha256(path)}
        print(f"  {name:6s} {len(parts[name]):5d} tin  ({n_spam} spam)")
    code = fingerprint(manifest)
    print(f"\nMÃ BỘ CHIA: {code}   (so mã này với cả team trong nhóm chat)")
    if MANIFEST.exists():
        print("Đối chiếu với manifest.json chung của team:")
        shared = json.loads(MANIFEST.read_text(encoding="utf-8"))
        if not compare(manifest, shared):
            raise SystemExit("Dữ liệu của bạn khác bản chung. Kiểm tra lại file gốc tải từ trang UCI.")
        print("Dữ liệu của bạn giống hệt cả team.")
    else:
        MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("Chưa có manifest.json chung: đã tạo. Nếu mã bộ chia khớp với cả team, "
              "người mở pull request đầu tiên commit file data/splits/manifest.json.")


def check() -> None:
    if not MANIFEST.exists():
        raise SystemExit("Chưa có manifest.json. Chạy: python scripts/make_splits.py")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    ok = True
    if RAW_FILE.exists() and "raw_sha256" in manifest:
        same_raw = sha256(RAW_FILE) == manifest["raw_sha256"]
        ok &= same_raw
        print(f"  raw    {'OK' if same_raw else 'KHÁC BẢN CHUNG (tải lại từ trang UCI)'}")
    for name, info in manifest["splits"].items():
        path = SPLITS_DIR / f"{name}.tsv"
        same = path.exists() and sha256(path) == info["sha256"]
        ok &= same
        print(f"  {name:6s} {'OK' if same else 'KHÁC BẢN CHUNG'}")
    raise SystemExit(0 if ok else "Có file khác bản chung (xem dòng KHÁC BẢN CHUNG ở trên).")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="chỉ kiểm tra, không tạo lại")
    args = parser.parse_args()
    check() if args.check else make()
