"""Xem từ xuất hiện nhiều trong spam so với ham trên tập train – gợi ý để viết luật.

  python scripts/top_words.py --n 20
"""
import argparse

import _bootstrap  # noqa: F401
from spam.data import load_split
from spam.preprocess import preprocess
from spam.rules import word_frequencies
from spam.schema import HAM, SPAM

parser = argparse.ArgumentParser()
parser.add_argument("--n", type=int, default=20)
parser.add_argument("--min-count", type=int, default=10)
args = parser.parse_args()

train = load_split("train")
freq = word_frequencies(train, preprocess)
n_spam = sum(m.label == SPAM for m in train)
n_ham = len(train) - n_spam
rows = []
for word, c_spam in freq[SPAM].items():
    if c_spam < args.min_count:
        continue
    rate_spam = c_spam / n_spam
    rate_ham = freq[HAM][word] / n_ham
    rows.append((rate_spam / (rate_ham + 1e-3), word, c_spam, freq[HAM][word]))
rows.sort(reverse=True)
print(f"{'Từ':14s} {'Lần trong spam':>15s} {'Lần trong ham':>14s}")
for _, word, c_spam, c_ham in rows[: args.n]:
    print(f"{word:14s} {c_spam:15d} {c_ham:14d}")
