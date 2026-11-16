from spam.metrics import confusion_matrix, report


def test_confusion_matrix_counts():
    y_true = ["spam", "spam", "ham", "ham", "ham"]
    y_pred = ["spam", "ham", "spam", "ham", "ham"]
    assert confusion_matrix(y_true, y_pred) == {"tp": 1, "fp": 1, "fn": 1, "tn": 2}


def test_report_values():
    r = report(["spam", "spam", "ham", "ham"], ["spam", "ham", "spam", "ham"])
    assert r["precision"] == 0.5 and r["recall"] == 0.5 and r["f1"] == 0.5 and r["accuracy"] == 0.5


def test_no_positive_prediction_does_not_crash():
    r = report(["spam", "ham"], ["ham", "ham"])
    assert r["precision"] == 0.0 and r["recall"] == 0.0 and r["f1"] == 0.0
