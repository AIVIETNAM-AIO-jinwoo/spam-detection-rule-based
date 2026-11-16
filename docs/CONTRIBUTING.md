# Quy ước làm việc

## Branch

- Không push thẳng lên `main`
- Tên branch bắt đầu bằng mã task Jira: `SCRUM-12-tokenizer`, `SCRUM-20-baseline-thuy`

## Commit

| Tiền tố | Khi nào | Ví dụ |
| --- | --- | --- |
| `feat:` | chức năng mới | `feat: add url detection rule` |
| `fix:` | sửa lỗi | `fix: handle empty message in preprocess` |
| `docs:` | tài liệu | `docs: update data card` |
| `test:` | thêm hoặc sửa test | `test: add metrics edge cases` |
| `refactor:` | chỉnh code, không đổi chức năng | `refactor: split RuleScorer weights` |
| `chore:` | việc nhỏ khác | `chore: update requirements` |

Không dùng `update`, `final`, `sửa bài`.

## Pull request

- Điền đủ mẫu trong `.github/pull_request_template.md`
- Người review là người làm bước kế tiếp trong pipeline:

| Phần | Người review |
| --- | --- |
| 1. Dữ liệu (Tuấn Duy) | Thúy |
| 2. Tiền xử lý (Thúy) | Duy Dương |
| 3. Thống kê và luật (Duy Dương) | Ngọc |
| 4. Đánh giá (Ngọc) | Leader |
| 5. Tích hợp và demo (Leader) | Tuấn Duy |

- Task chỉ được chuyển sang Done khi pull request đã được review, merge vào `main`, và `pytest` chạy qua
