# Spam Detection rule-based – Team Conquer

Hệ thống phát hiện tin nhắn spam bằng luật, kết hợp thống kê tần suất từ. Dự án Conquer Warmup, AIO2027.

## Bắt đầu nhanh (mọi thành viên)

```bash
git clone <repo-url> && cd spam-detection
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python scripts/download_data.py   # tải dữ liệu gốc về data/raw/
python scripts/make_splits.py     # tạo bộ chia trên máy bạn, in ra MÃ BỘ CHIA
pytest                            # kiểm tra mọi thứ chạy được
python scripts/evaluate.py pipeline --split dev
```

Ai cũng tự tạo bộ chia trên máy mình, không phải chờ ai. Bộ chia là tất định nên máy nào cũng ra cùng kết quả; cả team chỉ cần dán **mã bộ chia** vào nhóm chat để đối chiếu. Người mở pull request đầu tiên commit thêm `data/splits/manifest.json`; từ đó script và `pytest` tự đối chiếu với bản chung.

## Ba thứ cả team dùng chung

1. **Một bộ dữ liệu, một cách chia.** [SMS Spam Collection trên UCI](https://archive.ics.uci.edu/dataset/228/sms+spam+collection) là nguồn duy nhất, chia sẵn train / dev / test và 20 tin mẫu, đối chiếu bằng `data/splits/manifest.json`. Chi tiết: [data/README.md](data/README.md).
2. **Một hợp đồng giữa các bước.** Định nghĩa trong `spam/schema.py` và đầu mỗi module. Baseline cá nhân và dự án chính dùng chung hợp đồng này, nên ý tưởng trong baseline chuyển thẳng vào dự án chính được.
3. **Một thước đo.** `spam/metrics.py`, chạy qua `scripts/evaluate.py`. Mọi con số báo cáo trong team đều lấy từ đây.

## Cấu trúc

```text
spam/                  Dự án chính, mỗi file là một bước của pipeline
  schema.py            Hợp đồng dữ liệu: nhãn, Message, Prediction (cả team thống nhất mới được sửa)
  data.py              Bước 1 – Dữ liệu ............ Tuấn Duy
  preprocess.py        Bước 2 – Tiền xử lý ......... Thúy
  rules.py             Bước 3 – Thống kê và luật ... Duy Dương
  metrics.py           Bước 4 – Đánh giá ........... Ngọc
  pipeline.py          Bước 5 – Tích hợp ........... Leader
baselines/             Baseline cá nhân sprint 1 (xem baselines/README.md)
scripts/
  download_data.py     Tải và kiểm tra dữ liệu gốc
  make_splits.py       Tạo / kiểm tra bộ chia chung
  evaluate.py          Chấm baseline hoặc pipeline, lưu kết quả và tin đoán sai
  compare_results.py   Bảng so sánh mọi kết quả, dùng trong buổi demo
  top_words.py         Từ đặc trưng của spam trên tập train, gợi ý để viết luật
data/splits/           Bộ chia (tự tạo trên máy; chỉ commit manifest.json)
results/               Kết quả chấm (được commit, dùng để so sánh)
tests/                 Kiểm tra hợp đồng, metric, dữ liệu
```

## Hợp đồng giữa các bước

| Bước | Hàm | Vào | Ra |
| --- | --- | --- | --- |
| 1. Dữ liệu | `load_split(name)` | `"sample"`, `"train"`, `"dev"`, `"test"` | `list[Message]` |
| 2. Tiền xử lý | `preprocess(text)` | `str` | `list[str]` |
| 3. Luật | `RuleScorer.score(raw_text, tokens)` | `str`, `list[str]` | `(float, list[str])` điểm và lý do |
| 4. Đánh giá | `report(y_true, y_pred)` | hai `list[str]` | `dict` tp, fp, fn, tn, accuracy, precision, recall, f1 |
| 5. Tích hợp | `SpamPipeline.predict(text)` | `str` | `Prediction(label, score, reasons)` |

Nhãn luôn là chuỗi `"spam"` hoặc `"ham"`; lớp dương khi tính metric là `"spam"`. Muốn đổi hợp đồng: mở task trên Jira, thống nhất trong buổi check-in, rồi mới sửa.

## Ba quy tắc về dữ liệu

- **Train** để thống kê và viết luật. **Dev** để chọn ngưỡng và so sánh. **Test** chỉ chấm một lần ở cuối sprint 3 (`--final`).
- Không sửa file trong `data/splits/` bằng tay. `pytest` sẽ báo nếu bộ chia khác bản chung.
- Phân tích lỗi dùng danh sách tin đoán sai trong `results/*.json`, không dùng tập test.

Quy ước branch, commit và pull request: [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md).
