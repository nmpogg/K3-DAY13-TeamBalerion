# Template Alert và Runbook

Mỗi alert phải dựa trên triệu chứng người dùng hoặc SLO, không dựa trực tiếp vào tên implementation nội bộ.

## Alert 1

- **Tên:** high_latency_p95
- **Severity:** warning
- **SLI/SLO liên quan:** latency_p95_ms (Objective: 3000, Target: 99.5%)
- **Điều kiện và thời gian duy trì:** latency_p95 > 3000ms for 5 minutes
- **Ảnh hưởng tới người dùng:** Ứng dụng phản hồi chậm, người dùng phải chờ đợi lâu khi sử dụng chức năng chat, gây ức chế và có thể dẫn đến việc họ rời bỏ ứng dụng hoặc làm mới (refresh) trang.
- **Ba bước kiểm tra đầu tiên:**
  1. Kiểm tra Dashboard (Latency Metrics) và Langfuse Traces để xem bước nào trong pipeline chậm nhất (ví dụ: Retriever chậm hay LLM Generation chậm).
  2. Kiểm tra log ứng dụng xem có lỗi mạng, retry, hoặc timeout khi kết nối tới các dịch vụ bên ngoài (LLM provider, VectorDB) không.
  3. Kiểm tra lưu lượng truy cập (Traffic) xem hệ thống có đang quá tải hay thắt cổ chai tài nguyên (CPU/Memory) không.
- **Mitigation tạm thời:** Tắt các logic không cần thiết (ví dụ: metadata enrichers nặng), giảm bớt lượng documents truyền vào prompt, hoặc tự động scale-out thêm instances nếu lượng traffic tăng cao.
- **Owner:** on-call-engineer

## Alert 2

- **Tên:** elevated_error_rate
- **Severity:** critical
- **SLI/SLO liên quan:** error_rate_pct (Objective: 2, Target: 99.0%)
- **Điều kiện và thời gian duy trì:** error_rate_pct > 5 for 3 minutes
- **Ảnh hưởng tới người dùng:** Người dùng nhận được thông báo lỗi liên tục, yêu cầu chat bị gián đoạn hoàn toàn, chức năng chính của sản phẩm không thể sử dụng.
- **Ba bước kiểm tra đầu tiên:**
  1. Kiểm tra Metric `error_breakdown` trên Dashboard để khoanh vùng loại lỗi phổ biến (VD: `RateLimitError`, `Timeout`, `ValidationError`).
  2. Lấy `correlation_id` của các request lỗi, tra cứu Logs để xem chi tiết Stack Trace và lý do thất bại.
  3. Kiểm tra trạng thái của các Third-party APIs (LLM API có đang sập không, kết nối database có đứt không).
- **Mitigation tạm thời:** Rollback lại phiên bản code/prompt gần nhất nếu vừa có đợt triển khai (deploy). Bật fallback mode (ví dụ trả về câu trả lời tĩnh, sử dụng model dự phòng, hoặc thông báo hệ thống đang bảo trì).
- **Owner:** on-call-engineer

## Alert 3

- **Tên:** cost_budget_exceeded
- **Severity:** warning
- **SLI/SLO liên quan:** daily_cost_usd (Objective: 2.5, Target: 100.0%)
- **Điều kiện và thời gian duy trì:** daily_cost_usd > 2.5
- **Ảnh hưởng tới người dùng:** Không có ảnh hưởng trực tiếp đến người dùng cuối, nhưng dự án sẽ bị thâm hụt ngân sách nghiêm trọng và phát sinh chi phí không lường trước.
- **Ba bước kiểm tra đầu tiên:**
  1. Kiểm tra Dashboard (Metrics Traffic & Tokens) xem có sự gia tăng đột biến về lượng tokens (đặc biệt là output tokens) hoặc số lượng requests do bot/spam gây ra không.
  2. Xác minh xem hệ thống có vô tình sử dụng model có chi phí cao hơn dự kiến (ví dụ: Claude Opus thay vì Sonnet/Haiku) do cấu hình sai không.
  3. Kiểm tra độ lớn của context truyền vào LLM (số lượng documents từ RAG) có bị vượt kiểm soát không.
- **Mitigation tạm thời:** Tạm thời áp dụng Rate Limiting khắt khe hơn; hạ model xuống phiên bản rẻ hơn (như Claude Haiku); chặn IP/user đang có dấu hiệu spam, lạm dụng hệ thống.
- **Owner:** team-lead
