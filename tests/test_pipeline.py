from spam.pipeline import SpamPipeline
from spam.preprocess import preprocess


def test_preprocess_returns_list_of_str():
    tokens = preprocess("WIN a FREE prize now!!!")
    assert isinstance(tokens, list) and all(isinstance(t, str) for t in tokens)


def test_pipeline_obvious_cases():
    pipe = SpamPipeline()
    spam = pipe.predict("URGENT! You are a WINNER. Claim your FREE prize, call 09061701461 now")
    ham = pipe.predict("Ok see you at lunch tomorrow")
    assert spam.label == "spam" and spam.reasons
    assert ham.label == "ham"
