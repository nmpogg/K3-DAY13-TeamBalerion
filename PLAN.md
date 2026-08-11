# Kế hoạch thực hiện Lab (Nhóm 4 thành viên)

Kế hoạch này phân chia công việc theo vai trò chuyên môn của từng thành viên. Mọi người có thể tiến hành công việc song song hoặc nối tiếp tùy vào sự phụ thuộc của file.

## 👤 Thành viên A (Logging & Middleware): Phụ trách Checkpoint 1
Trần Hoàng Vũ - 2A202602000
**Vai trò:** Đảm bảo luồng request được theo dõi (traceable) và các log đầu ra có đầy đủ metadata ngữ cảnh.

- **Nhiệm vụ chi tiết:**
  - **Middleware & Correlation ID:** Cấu hình middleware để tạo và bắt `X-Correlation-ID` cho mỗi request.
  - **Log Metadata:** Trích xuất và gán các thông tin ngữ cảnh vào log (như `user_id_hash`, `session_id`, `feature`, `model`, `env`).
- **Các file cần sửa:**
  - `app/middleware.py`: Thêm logic gán/tạo Correlation ID.
  - `app/logging_config.py` (hoặc `app/main.py`): Sử dụng contextvars của structlog để bind các giá trị metadata vào log trước khi xuất ra.

## 👤 Thành viên B (Security & Compliance): Phụ trách Checkpoint 1
Nguyễn Thùy Trang - 2A202601559
**Vai trò:** Đảm bảo hệ thống tuân thủ bảo mật, không rò rỉ dữ liệu nhạy cảm (PII) của người dùng ra file log.

- **Nhiệm vụ chi tiết:**
  - **Che giấu PII (Masking):** Viết các biểu thức chính quy (Regex) để nhận diện và thay thế Email, số điện thoại, số thẻ tín dụng thành định dạng ẩn danh (ví dụ `***@gmail.com`).
  - **Kích hoạt Processor:** Kích hoạt tính năng lọc PII toàn cục cho hệ thống log.
- **Các file cần sửa:**
  - `app/pii.py`: Thêm các Regex patterns che PII.
  - `app/logging_config.py`: Uncomment processor liên quan đến PII và thêm nó vào chuỗi xử lý (processors list) của structlog.

## 👤 Thành viên C (Metrics & Alerting): Phụ trách Checkpoint 2
Nguyễn Văn Đại - 2A202601245
**Vai trò:** Đo lường hiệu năng hệ thống, tích hợp hệ thống Tracing và thiết lập cảnh báo khi hệ thống không đạt chuẩn.

- **Nhiệm vụ chi tiết:**
  - **Tích hợp Langfuse:** Gắn các decorator hoặc code tracking để đẩy trace lên Langfuse. Quản lý metadata của prompt (phiên bản, tên, nhãn).
  - **Đo đếm Metrics:** Bổ sung logic tính toán phần trăm lỗi (`error_rate_pct`).
  - **SLO & Alerts:** Định nghĩa các ngưỡng chấp nhận được (SLO), tạo Alert rules và viết Runbook xử lý khi có cảnh báo.
- **Các file cần sửa:**
  - `app/agent.py` và `app/tracing.py`: Thêm code tích hợp Langfuse.
  - `app/metrics.py`: Tính toán metric `error_rate_pct`.
  - `config/slo.yaml` & `config/alert_rules.yaml`: Viết quy tắc cấu hình SLO và Alert.
  - `docs/alerts.md` (hoặc tạo file Runbook mới): Viết quy trình xử lý sự cố.

## 👤 Thành viên D (QA & Incident Analyst): Phụ trách Checkpoint 3 & Setup ban đầu
Ngô Minh Phong - 2A202602025
**Vai trò:** Đảm bảo hệ thống có dữ liệu để test, thiết kế công cụ quan sát (Dashboard) và chủ trì giải quyết sự cố thực tế (Challenge).

- **Nhiệm vụ chi tiết:**
  - **Tạo dữ liệu:** Chạy load test để sinh ra log và trace cho toàn hệ thống.
  - **Dashboard Spec:** Thiết kế Dashboard hiển thị Metrics (Traffic, Latency, Error, Cost/Token).
  - **Incident Analyst (Challenge CP3):** Quan sát Dashboard để tìm dấu hiệu bất thường, dùng Trace khoanh vùng lỗi, đọc Log tìm Root cause.
  - **Viết báo cáo:** Tổng hợp nguyên nhân và giải pháp vào Report.
- **Các file cần sửa/thao tác:**
  - Chạy lệnh: `python scripts/load_test.py`
  - `config/dashboard.yaml`: Cấu hình Dashboard Spec (tham khảo `docs/dashboard-spec.md`).
  - `submission/REPORT.md`: Viết báo cáo sự cố (CP3) và hoàn thiện các evidence (chụp ảnh màn hình lưu vào `submission/evidence/`).
