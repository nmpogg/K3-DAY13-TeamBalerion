# Báo cáo Day 13 Observability

## 1. Thông tin nhóm

- Tên nhóm: Balerion
- Repository URL: https://github.com/nmpogg/K3-DAY13-TeamBalerion
- Commit SHA cuối: 
- Thành viên và vai trò:

## 2. Kết quả kỹ thuật

- Điểm `validate_logs.py`: 100/100
- Tổng số traces: 148
- Số PII leak còn lại: 0
- Link/đường dẫn dashboard: `submission/evidence/dashboard.png`

## 3. Logging và tracing

- Evidence correlation ID: Đã bắt header `x-request-id` ở `app/middleware.py` và lưu vào structlog contextvars. Mọi log (request_received, response_sent, request_failed) đều có chung một `correlation_id`.
- Evidence PII redaction: Đã triển khai hàm `scrub_event` duyệt qua mọi trường để biến email/thẻ thành dạng ẩn danh (ví dụ `***@gmail.com`).
- Evidence trace waterfall: `submission/evidence/waterfall.png`
- Giải thích một span đáng chú ý: Span `retrieve` (Vector Store) đôi khi tốn 2.5s do sự cố `rag_slow` được kích hoạt, làm nghẽn toàn bộ quá trình trả lời của agent.

## 4. Prompt versioning

- Prompt name: `day13-chat`
- Version/label baseline: `v1` (production)
- Version/label candidate: `v2` (candidate)
- Trace ID của mỗi version: `14867eb3d265d751739b7d4460b015dc`, `27cba8a2a73a14a497a051e14e5e4ef5`
- Bằng chứng đổi label hoặc rollback: `submission/evidence/prompt.png`

## 5. Dashboard, SLO và alerts

- Kết quả `validate_dashboard.py`: HỢP LỆ (6/6 panel có trong dashboard contract).
- Evidence dashboard: `submission/evidence/dashboard.png`
- SLO đã chọn và lý do: `Latency P95 < 2s` (Người dùng không thích chờ đợi quá lâu khi chat bot), và `Error Rate < 5%` (Mức độ tin cậy cơ bản cho ứng dụng nội bộ).
- Alert rules và runbook: Đã cấu hình các rule cảnh báo trong `config/alert_rules.yaml` và quy trình xử lý sự cố trong `docs/alerts.md`.

## 6. Điều tra challenge

- Challenge ID: `day13-k3-observability-v1`
- Triệu chứng từ metrics: P50 và P95 Latency tăng vọt (lên tới >3500ms, thậm chí có request mất tới >19000ms) đặc biệt khi có tải đồng thời (concurrency = 5).
- Trace ID liên quan: c223c5b4a3c7f69158835a681d422c8b
- Log line/correlation ID liên quan: Ví dụ `req-9bfa6774`, `req-2654c830` (những request tốn 15-19 giây).
- Root cause: Sự cố `rag_slow` làm hàm `retrieve` bị chậm. Tuy nhiên, nguyên nhân gốc rễ gây ra chậm đến 19 giây là do endpoint `/chat` trong `app/main.py` được khai báo là `async def` nhưng lại gọi một hàm đồng bộ (blocking) là `agent.run()` (bên trong chứa `time.sleep`). Việc này làm "đóng băng" (block) toàn bộ event loop của FastAPI. Thay vì chạy song song, 5 request phải xếp hàng chạy nối đuôi nhau.
- Fix action: Xóa chữ `async` ở định nghĩa hàm `async def chat(...)` trong `app/main.py` (trở thành `def chat(...)`). Nhờ vậy FastAPI sẽ tự động đưa các request này vào một Threadpool để chạy song song mà không block event loop chính.
- Preventive measure: Thiết lập Alert cảnh báo khi Latency P95 vượt ngưỡng 2s. Trong quy trình Code Review, cần kiểm tra nghiêm ngặt không cho phép gọi hàm đồng bộ (I/O blocking) trực tiếp bên trong các hàm `async def` mà không dùng threadpool hoặc `asyncio`.

## 7. Đóng góp cá nhân

Với mỗi thành viên, ghi rõ nhiệm vụ và link commit/PR tương ứng.

| Thành viên | Phần việc | Commit/PR | Điều đã học |
|---|---|---|---|
| | | | |
