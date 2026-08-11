# Yêu cầu dashboard

Contract có thể kiểm tra bằng máy nằm tại `config/dashboard.yaml`. Hướng dẫn dựng và kiểm tra runtime nằm tại [DASHBOARD_SETUP.md](DASHBOARD_SETUP.md).

Dashboard chính cần đủ 6 nhóm thông tin:

1. Latency P50/P95/P99.
2. Traffic: request count hoặc QPS.
3. Error rate và breakdown theo loại lỗi.
4. Cost theo thời gian.
5. Tổng token input/output.
6. Quality proxy.

Tiêu chuẩn trình bày:

- Khoảng thời gian mặc định: 1 giờ.
- Tự refresh mỗi 15–30 giây nếu công cụ hỗ trợ.
- Có threshold hoặc SLO line.
- Ghi rõ đơn vị.
- Chỉ giữ 6–8 panel quan trọng ở lớp chính.
- Screenshot phải nhìn được tên panel và khoảng thời gian.

Kiểm tra contract trước khi chụp evidence:

```bash
python scripts/validate_dashboard.py
```

## Đặc tả Dashboard (Dashboard Spec)

Công cụ sử dụng: **Langfuse Dashboard**
Khoảng thời gian mặc định cho tất cả các panel: **1 giờ** (1h)

| Nhóm | Tên Panel | Nguồn Dữ Liệu | Đơn vị | Threshold / SLO Line |
|---|---|---|---|---|
| **1. Latency** | Hệ thống Latency (P50/P95/P99) | `/metrics` → `latency_p50`, `latency_p95`, `latency_p99` | Giây (s) | SLO: P95 < 2.0s |
| **2. Traffic** | Tổng số lượng Request | `/metrics` → `traffic` | Requests (count) | N/A |
| **3. Error** | Tỷ lệ lỗi (Error Rate) & Phân bổ | `/metrics` → `error_rate_pct`, `error_breakdown` | Phần trăm (%) | SLO: Error Rate < 5% |
| **4. Cost** | Chi phí LLM (Total & Avg) | `/metrics` → `total_cost_usd`, `avg_cost_usd` | USD ($) | Ngưỡng: Total > $10 |
| **5. Tokens** | Tiêu thụ Token (Input/Output) | `/metrics` → `tokens_in_total`, `tokens_out_total` | Tokens (count) | N/A |
| **6. Quality** | Điểm chất lượng trung bình | `/metrics` → `quality_avg` | Điểm (0-1) | SLO: Quality > 0.8 |

> **Evidence:** Spec này tương thích với khai báo trong file `config/dashboard.yaml`. Để có evidence, nhóm (Thành viên D) cần dùng giao diện Langfuse tạo 1 dashboard chứa các panel y hệt bảng trên, sau đó chụp màn hình (nhớ lấy cả khoảng thời gian 1h) rồi lưu vào `submission/evidence/`.
