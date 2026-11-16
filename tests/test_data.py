"""Kiểm tra bộ chia dữ liệu chung (bỏ qua nếu chưa tạo)."""
import hashlib
import json
from pathlib import Path

import pytest

from spam.data import SPLITS_DIR, load_split

MANIFEST = SPLITS_DIR / "manifest.json"
NAMES = ("train", "dev", "test", "sample")
pytestmark = pytest.mark.skipif(
    not MANIFEST.exists() or not all((SPLITS_DIR / f"{n}.tsv").exists() for n in NAMES),
    reason="chưa có bộ chia trên máy: chạy python scripts/make_splits.py",
)


def test_files_match_manifest():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for name, info in manifest["splits"].items():
        digest = hashlib.sha256(Path(SPLITS_DIR / f"{name}.tsv").read_bytes()).hexdigest()
        assert digest == info["sha256"], f"{name}.tsv khác bản chung"


def test_no_text_leaks_between_splits():
    texts = {name: {m.text for m in load_split(name)} for name in ("train", "dev", "test")}
    assert not texts["train"] & texts["dev"]
    assert not texts["train"] & texts["test"]
    assert not texts["dev"] & texts["test"]
