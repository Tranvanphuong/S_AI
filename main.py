import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from supabase import create_client, Client
from typing import List, Optional
from datetime import datetime
import pandas as pd

# Đọc cấu hình Supabase từ biến môi trường
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://helztticlepdbkvdlyuo.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhlbHp0dGljbGVwZGJrdmRseXVvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MjAzMzcyMiwiZXhwIjoyMDY3NjA5NzIyfQ.aX3QPAHhkyC2-MkMMhjHLgARuCpRLUWzLyqWFeV2RnI")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="Payroll Management API")

# Helper: Chuyển YYYY-MM thành ngày đầu tháng
def parse_month(month_str: str) -> str:
    try:
        return datetime.strptime(month_str, "%Y-%m").strftime("%Y-%m-01")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid month format, must be YYYY-MM")

@app.post("/api/calculate-salary")
async def calculate_salary(file: UploadFile = File(...)):
    # TODO: Đọc file Excel/CSV, parse, tính lương, insert vào payrolls
    # Giả lập kết quả trả về
    return {
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

@app.get("/api/salary/{employee_id}/{month}")
def get_salary(employee_id: str, month: str):
    month_date = parse_month(month)
    res = supabase.table("payrolls").select("*").eq("employee_id", employee_id).eq("month", month_date).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Payroll not found")
    payroll = res.data[0]
    return {
        "employee_id": payroll["employee_id"],
        "month": month,
        "gross_salary": payroll["gross_salary"],
        "tax": payroll["tax"],
        "insurance": payroll["insurance"],
        "net_salary": payroll["net_salary"],
        "overtime_hours": payroll.get("overtime_hours", 0),
        "leave_days": payroll.get("leave_days", 0)
    }

@app.get("/api/compare-salary/{employee_id}")
def compare_salary(employee_id: str, from_: str, to: str):
    from_month = parse_month(from_)
    to_month = parse_month(to)
    res_from = supabase.table("payrolls").select("*").eq("employee_id", employee_id).eq("month", from_month).execute()
    res_to = supabase.table("payrolls").select("*").eq("employee_id", employee_id).eq("month", to_month).execute()
    if not res_from.data or not res_to.data:
        raise HTTPException(status_code=404, detail="Payroll not found for one or both months")
    p_from = res_from.data[0]
    p_to = res_to.data[0]
    gross_diff = p_to["gross_salary"] - p_from["gross_salary"]
    net_diff = p_to["net_salary"] - p_from["net_salary"]
    status = "increase" if net_diff > 0 else "decrease" if net_diff < 0 else "nochange"
    return {
        "employee_id": employee_id,
        "from": from_,
        "to": to,
        "gross_salary_diff": gross_diff,
        "net_salary_diff": net_diff,
        "status": status
    }

@app.get("/api/overtime/{employee_id}/{month}")
def get_overtime(employee_id: str, month: str):
    month_date = parse_month(month)
    res = supabase.table("payrolls").select("*").eq("employee_id", employee_id).eq("month", month_date).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Payroll not found")
    payroll = res.data[0]
    return {
        "employee_id": payroll["employee_id"],
        "month": month,
        "overtime_hours": payroll.get("overtime_hours", 0),
        "overtime_pay": payroll.get("overtime_pay", 0)
    }

@app.get("/api/report/salary-summary")
def salary_summary(month: str):
    month_date = parse_month(month)
    res = supabase.table("payrolls").select("net_salary").eq("month", month_date).execute()
    total = sum([row["net_salary"] for row in res.data]) if res.data else 0
    return {
        "month": month,
        "total_payroll": total
    }

@app.get("/api/report/department")
def report_department(month: str):
    month_date = parse_month(month)
    # Lấy payrolls + join employees + departments
    payrolls = supabase.table("payrolls").select("employee_id,net_salary").eq("month", month_date).execute().data
    if not payrolls:
        return {"month": month, "departments": []}
    # Lấy thông tin nhân viên
    emp_ids = [p["employee_id"] for p in payrolls]
    employees = supabase.table("employees").select("employee_id,department_id").in_("employee_id", emp_ids).execute().data
    dept_ids = list(set([e["department_id"] for e in employees]))
    departments = supabase.table("departments").select("department_id,name").in_("department_id", dept_ids).execute().data
    # Mapping
    emp_dept = {e["employee_id"]: e["department_id"] for e in employees}
    dept_name = {d["department_id"]: d["name"] for d in departments}
    dept_salary = {}
    for p in payrolls:
        dept_id = emp_dept.get(p["employee_id"])
        if dept_id:
            dept_salary.setdefault(dept_id, 0)
            dept_salary[dept_id] += p["net_salary"]
    result = [{"department": dept_name[dept_id], "total_salary": total} for dept_id, total in dept_salary.items()]
    return {
        "month": month,
        "departments": result
    }

@app.post("/api/report/export")
def export_report(format: str, month: str):
    # TODO: Truy vấn payrolls, xuất file PDF/Excel, trả về file response
    return JSONResponse({"message": "Export report feature is not implemented yet."})

# Hướng dẫn cấu hình Supabase:
# - Đặt biến môi trường SUPABASE_URL và SUPABASE_KEY trước khi chạy app.
# - Ví dụ export SUPABASE_URL=https://xyzcompany.supabase.co
#         export SUPABASE_KEY=YOUR_API_KEY

@app.post("/api/import-employees")
async def import_employees(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Chỉ hỗ trợ file .csv")
    try:
        df = pd.read_csv(file.file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Lỗi đọc file CSV: {str(e)}")
    required_cols = {"employee_id", "full_name", "department"}
    if not required_cols.issubset(df.columns):
        raise HTTPException(status_code=400, detail=f"File CSV phải có các cột: {', '.join(required_cols)}")
    # Lấy mapping tên phòng ban -> department_id
    depts = supabase.table("departments").select("department_id,name").execute().data
    dept_map = {d["name"]: d["department_id"] for d in depts}
    # Lấy danh sách employee_id đã có
    existing_emps = supabase.table("employees").select("employee_id").execute().data
    existing_ids = set(e["employee_id"] for e in existing_emps)
    success, failed = 0, 0
    errors = []
    for idx, row in df.iterrows():
        try:
            employee_id = str(row["employee_id"]).strip()
            full_name = str(row["full_name"]).strip()
            department_name = str(row["department"]).strip()
            position = str(row["position"]).strip() if "position" in df.columns and pd.notna(row["position"]) else None
            date_of_birth = str(row["date_of_birth"]).strip() if "date_of_birth" in df.columns and pd.notna(row["date_of_birth"]) else None
            date_joined = str(row["date_joined"]).strip() if "date_joined" in df.columns and pd.notna(row["date_joined"]) else None
            is_active = row["is_active"] if "is_active" in df.columns and pd.notna(row["is_active"]) else True
            # Validate bắt buộc
            if not employee_id or not full_name or not department_name:
                raise Exception("Thiếu thông tin bắt buộc (employee_id, full_name, department)")
            if employee_id in existing_ids:
                raise Exception(f"employee_id {employee_id} đã tồn tại")
            if department_name not in dept_map:
                raise Exception(f"Phòng ban '{department_name}' không tồn tại")
            department_id = dept_map[department_name]
            # Validate ngày tháng
            if date_of_birth:
                try:
                    date_of_birth = str(pd.to_datetime(date_of_birth).date())
                except Exception:
                    raise Exception("date_of_birth không hợp lệ (YYYY-MM-DD)")
            else:
                date_of_birth = None
            if date_joined:
                try:
                    date_joined = str(pd.to_datetime(date_joined).date())
                except Exception:
                    raise Exception("date_joined không hợp lệ (YYYY-MM-DD)")
            else:
                date_joined = None
            # Validate is_active
            if isinstance(is_active, str):
                is_active_val = is_active.strip().lower()
                if is_active_val in ["true", "1", "yes"]:
                    is_active = True
                elif is_active_val in ["false", "0", "no"]:
                    is_active = False
                else:
                    raise Exception("is_active phải là TRUE/FALSE")
            else:
                is_active = bool(is_active)
            # Insert vào employees
            res = supabase.table("employees").insert({
                "employee_id": employee_id,
                "full_name": full_name,
                "department_id": department_id,
                "position": position,
                "date_of_birth": date_of_birth,
                "date_joined": date_joined,
                "is_active": is_active
            }).execute()
            # if res.status_code >= 400:
            #     raise Exception(res.data.get("message", "Lỗi khi insert"))
            success += 1
            existing_ids.add(employee_id)
        except Exception as e:
            failed += 1
            errors.append({"row": int(idx)+2, "error": str(e)})
    return {
        "total": len(df),
        "success": success,
        "failed": failed,
        "errors": errors
    }

@app.post("/api/import-attendance")
async def import_attendance(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Chỉ hỗ trợ file .csv")
    try:
        df = pd.read_csv(file.file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Lỗi đọc file CSV: {str(e)}")
    required_cols = {"employee_id", "work_date", "check_in", "check_out", "work_type", "note"}
    if not required_cols.issubset(df.columns):
        raise HTTPException(status_code=400, detail=f"File CSV phải có đủ các cột: {', '.join(required_cols)}")
    success, failed = 0, 0
    errors = []
    for idx, row in df.iterrows():
        try:
            # Validate dữ liệu cơ bản
            employee_id = str(row["employee_id"]).strip()
            work_date = str(row["work_date"]).strip()
            check_in = str(row["check_in"]).strip() if pd.notna(row["check_in"]) and row["check_in"] else None
            check_out = str(row["check_out"]).strip() if pd.notna(row["check_out"]) and row["check_out"] else None
            work_type = str(row["work_type"]).strip() if pd.notna(row["work_type"]) else None
            note = str(row["note"]).strip() if pd.notna(row["note"]) else None
            # Kiểm tra employee_id tồn tại
            emp = supabase.table("employees").select("employee_id").eq("employee_id", employee_id).execute()
            if not emp.data:
                raise Exception(f"employee_id {employee_id} không tồn tại")
            # Insert vào attendance_details
            res = supabase.table("attendance_details").insert({
                "employee_id": employee_id,
                "work_date": work_date,
                "check_in": check_in,
                "check_out": check_out,
                "work_type": work_type,
                "note": note
            }).execute()
            # if res.status_code >= 400:
            #     raise Exception(res.data.get("message", "Lỗi khi insert"))
            success += 1
        except Exception as e:
            failed += 1
            errors.append({"row": int(idx)+2, "error": str(e)})  # +2 vì header + index 0
    return {
        "total": len(df),
        "success": success,
        "failed": failed,
        "errors": errors
    }
