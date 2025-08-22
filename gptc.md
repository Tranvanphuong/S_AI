# Kế hoạch thi công chi tiết cho hệ thống quản lý lương sử dụng LangGraph


## Todo List


- [ ] Phân tích yêu cầu chi tiết và thiết kế kiến trúc hệ thống
- [ ] Thiết lập cơ sở dữ liệu với các bảng: employees, timesheets, payroll
- [ ] Xây dựng API backend:
  - [ ] POST /api/calculate-salary: nhận file chấm công, parse và tính lương
  - [ ] GET /api/salary/{employee_id}/{month}: lấy chi tiết lương nhân viên
  - [ ] GET /api/compare-salary/{employee_id}: so sánh lương giữa 2 tháng
  - [ ] GET /api/overtime/{employee_id}/{month}: tính tiền OT
  - [ ] GET /api/report/salary-summary: tổng quỹ lương theo tháng
  - [ ] GET /api/report/department: chi phí lương theo phòng ban
  - [ ] POST /api/report/export: xuất báo cáo file PDF/Excel
- [ ] Xây dựng LangGraph Agent:
  - [ ] Xử lý upload file chấm công, parse thành JSON
  - [ ] Gọi API tính lương và trả kết quả
  - [ ] Phân loại intent câu hỏi chatbot, gọi API dữ liệu phù hợp
  - [ ] Trả lời chatbot bằng text hoặc biểu đồ
- [ ] Xây dựng giao diện người dùng:
  - [ ] UI chat hỗ trợ phiên làm việc
  - [ ] Upload file chấm công
  - [ ] Hiển thị kết quả bảng lương, báo cáo
  - [ ] Hiển thị biểu đồ so sánh, xu hướng lương
- [ ] Kiểm thử toàn bộ hệ thống:
  - [ ] Test upload file và tính lương
  - [ ] Test chatbot hỏi đáp
  - [ ] Test báo cáo và xuất file
- [ ] Triển khai và hướng dẫn sử dụng