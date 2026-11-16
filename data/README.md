# Thẻ dữ liệu

## Nguồn duy nhất của team

**SMS Spam Collection**, UCI Machine Learning Repository

- Trang dữ liệu: https://archive.ics.uci.edu/dataset/228/sms+spam+collection
- File tải: https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip (script `download_data.py` dùng link này)
- DOI: https://doi.org/10.24432/C5CC84
- Giấy phép: Creative Commons Attribution 4.0 (CC BY 4.0), được dùng và chỉnh sửa, miễn là ghi nguồn

Không dùng bản trên Kaggle, Hugging Face hay gói `ucimlrepo`: định dạng, mã hóa hoặc cách đọc có thể khác, làm lệch số liệu giữa các thành viên. Mã SHA-256 của file gốc được lưu trong `splits/manifest.json`; `make_splits.py --check` sẽ báo nếu file của bạn khác bản chung.

Trích dẫn khi dùng trong báo cáo:

> Almeida, T. & Hidalgo, J. (2011). SMS Spam Collection [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CC84

> Almeida, T.A., Gómez Hidalgo, J.M., Yamakami, A. Contributions to the Study of SMS Spam Filtering: New Collection and Results. Proceedings of the 2011 ACM Symposium on Document Engineering (DOCENG'11), Mountain View, CA, USA, 2011.

## Đặc điểm

- 5.574 tin nhắn SMS tiếng Anh: 4.827 ham (86,6%) và 747 spam (13,4%)
- Định dạng gốc: mỗi dòng `nhãn<TAB>nội dung`, nhãn là `ham` hoặc `spam`
- Dữ liệu lệch lớp: một bộ lọc đoán tất cả là ham vẫn đạt accuracy khoảng 87%, nên team báo cáo precision, recall, F1

## Cách chia (scripts/make_splits.py)

1. Chuẩn hóa khoảng trắng, bỏ tin trùng nội dung để cùng một tin không nằm ở cả train và test
2. Chia phân tầng theo nhãn: 70% train, 15% dev, 15% test, seed 42
3. `sample.tsv`: 10 spam và 10 ham lấy từ train, dùng cho baseline sprint 1

Mỗi người tự chạy script trên máy mình. Số lượng sau khi chia, mã SHA-256 của file gốc và của từng file chia nằm trong `splits/manifest.json`, file duy nhất của thư mục này được commit.

| File | Dùng để |
| --- | --- |
| `sample.tsv` | Chạy thử baseline, kiểm tra code |
| `train.tsv` | Thống kê tần suất, chọn từ khóa, viết luật |
| `dev.tsv` | Chọn ngưỡng, so sánh baseline, phân tích lỗi |
| `test.tsv` | Chấm một lần duy nhất ở cuối sprint 3 |

## Phần mở rộng (Stretch)

Tập tin nhắn tiếng Việt nhỏ, nếu làm, đặt ở `data/vi/` với cùng định dạng TSV và có thẻ dữ liệu riêng.
