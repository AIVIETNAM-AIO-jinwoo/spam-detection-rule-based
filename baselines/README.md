# Baseline cá nhân – Sprint 1

Mỗi thành viên tự viết một bản tối giản chạy đủ 5 bước, để ai cũng hiểu toàn bộ pipeline trước khi đi sâu vào phần của mình.

## Cách làm

1. Tạo branch: `SCRUM-<mã task>-baseline-<ten-ban>`
2. Copy `_template.py` thành `<ten-ban>.py` (viết thường, không dấu: `thuy.py`, `tuan-duy.py`)
3. Đổi `NAME`, viết `preprocess`, `score`, `my_report`
4. Chạy trên 20 tin mẫu, sửa đến khi không lỗi:
   `python scripts/evaluate.py baselines/<ten-ban>.py --split sample`
5. Chạy trên tập dev để có số liệu so sánh:
   `python scripts/evaluate.py baselines/<ten-ban>.py --split dev`
6. Chạy test: `pytest`
7. Mở pull request, đính kèm kết quả trên dev

## Hợp đồng bắt buộc

| Thành phần | Yêu cầu |
| --- | --- |
| `NAME` | chuỗi, trùng tên file, viết thường không dấu |
| `predict(text) -> str` | chỉ trả về `"spam"` hoặc `"ham"` |
| `my_report(y_true, y_pred) -> dict` | nên có; khóa `tp fp fn tn precision recall f1` |

## Không được làm

- Không đọc tập `test` dưới bất kỳ hình thức nào
- Không chép code của bạn khác; đọc để học thì được, sau đó tự viết
- Không dùng thư viện ngoài (sklearn, pandas…) trong baseline sprint 1
