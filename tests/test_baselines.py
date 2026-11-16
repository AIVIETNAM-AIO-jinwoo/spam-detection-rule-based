"""Kiểm tra mọi baseline trong baselines/ đúng hợp đồng (bỏ qua file bắt đầu bằng '_')."""
import importlib.util
from pathlib import Path

import pytest

from spam.metrics import report

BASELINE_DIR = Path(__file__).resolve().parent.parent / "baselines"
FILES = sorted(p for p in BASELINE_DIR.glob("*.py") if not p.name.startswith("_"))
TEXTS = ["Ok see you at lunch", "WINNER!! Claim your FREE prize now", "", "Call me later?"]


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("path", FILES, ids=[p.stem for p in FILES])
def test_contract(path):
    module = load(path)
    assert isinstance(module.NAME, str) and module.NAME == path.stem, "NAME phải trùng tên file"
    for text in TEXTS:
        assert module.predict(text) in ("spam", "ham")


@pytest.mark.parametrize("path", FILES, ids=[p.stem for p in FILES])
def test_my_report_matches_reference(path):
    module = load(path)
    if not hasattr(module, "my_report"):
        pytest.skip("chưa có my_report")
    y_true = ["spam", "spam", "ham", "ham", "ham", "spam"]
    y_pred = ["spam", "ham", "spam", "ham", "ham", "spam"]
    ref, mine = report(y_true, y_pred), module.my_report(y_true, y_pred)
    for key in ("tp", "fp", "fn", "tn", "precision", "recall", "f1"):
        assert abs(float(mine[key]) - float(ref[key])) < 1e-9, f"{key} lệch thước đo chung"
