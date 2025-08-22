 1. Tính toán lương


Mô tả:

HR upload file chấm công (Excel/CSV) → hệ thống tính lương gross, net, thuế, bảo hiểm → trả về kết quả.


Luồng xử lý:




Upload file → AI/Tool parse ra JSON.


Agent gọi API calculate_salary(file) → trả về danh sách bảng lương.


Xuất kết quả ra:


Text: “Tổng quỹ lương tháng 08: 1.2 tỷ VNĐ”


File: Excel/PDF bảng lương.



API cần có:




POST /api/calculate-salary → input file, output bảng lương JSON.


GET /api/salary/{employee_id}/{month} → lấy chi tiết lương 1 nhân viên.



DB liên quan:




employees(id, name, position, base_salary, department)


timesheets(employee_id, date, hours_worked, overtime_hours, leave_days)


payroll(employee_id, month, gross_salary, tax, insurance, net_salary)




 2. Chatbot hỏi đáp về lương


Mô tả:

Nhân viên / HR có thể hỏi Agent các câu tự nhiên:




“Lương tháng này của tôi bao nhiêu?”


“So với tháng trước tăng hay giảm?”


“OT tính bao nhiêu tiền?”



Luồng xử lý:




Người dùng nhập câu hỏi → LangGraph Agent → phân loại intent.


Nếu cần dữ liệu → gọi Tool API (DB).


Agent trả lời bằng text hoặc biểu đồ.



API cần có:




GET /api/salary/{employee_id}/{month} → lấy chi tiết lương.


GET /api/compare-salary/{employee_id}?from=2025-07&to=2025-08 → so sánh lương giữa 2 tháng.


GET /api/overtime/{employee_id}/{month} → tính OT.




 3. Báo cáo lương


Mô tả:

Hệ thống tạo báo cáo tổng hợp cho HR/Finance:




Tổng quỹ lương theo tháng.


Chi phí lương theo phòng ban.


Biểu đồ xu hướng tăng/giảm.



Luồng xử lý:




User yêu cầu: “Xuất báo cáo tháng 08”.


Agent gọi API → tổng hợp dữ liệu → sinh:


Biểu đồ (line chart, bar chart, pie chart).


File PDF/Excel báo cáo.



API cần có:




GET /api/report/salary-summary?month=2025-08 → tổng quỹ lương.


GET /api/report/department?month=2025-08 → chi phí lương theo phòng ban.


POST /api/report/export?format=pdf&month=2025-08 → xuất báo cáo file.