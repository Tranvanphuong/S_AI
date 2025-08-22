# API Backend Specifications for Payroll Management System


## 1. POST /api/calculate-salary
- Description: Upload timesheet file (Excel/CSV), parse and calculate payroll.
- Input: Multipart/form-data with field "file" containing the timesheet file.
- Output: JSON object with payroll list and total payroll amount.
- Response Example:
```json
{
  "month": "2025-08",
  "total_payroll": 1200000000,
  "payrolls": [
    {
      "employee_id": "E001",
      "gross_salary": 15000000,
      "tax": 1500000,
      "insurance": 1000000,
      "net_salary": 12500000
    }
  ]
}
```


## 2. GET /api/salary/{employee_id}/{month}
- Description: Get detailed payroll for an employee in a specific month.
- Input: 
  - Path parameters: `employee_id` (string), `month` (YYYY-MM)
- Output: JSON object with payroll details.
- Response Example:
```json
{
  "employee_id": "E001",
  "month": "2025-08",
  "gross_salary": 15000000,
  "tax": 1500000,
  "insurance": 1000000,
  "net_salary": 12500000,
  "overtime_hours": 10,
  "leave_days": 2
}
```


## 3. GET /api/compare-salary/{employee_id}?from=YYYY-MM&to=YYYY-MM
- Description: Compare payroll between two months for an employee.
- Input: 
  - Path parameter: `employee_id` (string)
  - Query parameters: `from` (YYYY-MM), `to` (YYYY-MM)
- Output: JSON object showing salary difference and status.
- Response Example:
```json
{
  "employee_id": "E001",
  "from": "2025-07",
  "to": "2025-08",
  "gross_salary_diff": 1000000,
  "net_salary_diff": 800000,
  "status": "increase"
}
```


## 4. GET /api/overtime/{employee_id}/{month}
- Description: Get overtime hours and pay for an employee in a month.
- Input: 
  - Path parameters: `employee_id` (string), `month` (YYYY-MM)
- Output: JSON object with OT hours and pay.
- Response Example:
```json
{
  "employee_id": "E001",
  "month": "2025-08",
  "overtime_hours": 10,
  "overtime_pay": 2000000
}
```


## 5. GET /api/report/salary-summary?month=YYYY-MM
- Description: Get total payroll for a month.
- Input: Query parameter: `month` (YYYY-MM)
- Output: JSON object with total payroll.
- Response Example:
```json
{
  "month": "2025-08",
  "total_payroll": 1200000000
}
```


## 6. GET /api/report/department?month=YYYY-MM
- Description: Get payroll cost by department for a month.
- Input: Query parameter: `month` (YYYY-MM)
- Output: JSON array of departments with total salary.
- Response Example:
```json
{
  "month": "2025-08",
  "departments": [
    {
      "department": "Sales",
      "total_salary": 500000000
    },
    {
      "department": "IT",
      "total_salary": 400000000
    }
  ]
}
```


## 7. POST /api/report/export?format=pdf|excel&month=YYYY-MM
- Description: Export payroll report as PDF or Excel file.
- Input: Query parameters: `format` (pdf or excel), `month` (YYYY-MM)
- Output: File response with appropriate content-type.