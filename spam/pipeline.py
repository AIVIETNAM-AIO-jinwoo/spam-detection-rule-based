"""Bước 5 – Tích hợp (phụ trách: Leader). Ghép các bước thành một pipeline."""
from spam.preprocess import preprocess
from spam.rules import RuleScorer
from spam.schema import HAM, SPAM, Prediction


class SpamPipeline:
    def __init__(self, preprocess_fn=preprocess, scorer=None, threshold: float = 2.0):
        self.preprocess_fn = preprocess_fn
        self.scorer = scorer or RuleScorer()
        self.threshold = threshold  # TODO(Ngọc): chọn ngưỡng bằng quét trên tập dev

    def predict(self, text: str) -> Prediction:
        tokens = self.preprocess_fn(text)
        score, reasons = self.scorer.score(text, tokens)
        return Prediction(label=SPAM if score >= self.threshold else HAM, score=score, reasons=reasons)

    def predict_many(self, texts) -> list:
        return [self.predict(t) for t in texts]
