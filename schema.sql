CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE employees (
    employee_id VARCHAR(10) PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    department_id INTEGER NOT NULL REFERENCES departments(department_id),
    position VARCHAR(50),
    date_of_birth DATE,
    date_joined DATE,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE payrolls (
    payroll_id SERIAL PRIMARY KEY,
    employee_id VARCHAR(10) NOT NULL REFERENCES employees(employee_id),
    month DATE NOT NULL,
    gross_salary NUMERIC NOT NULL,
    tax NUMERIC NOT NULL,
    insurance NUMERIC NOT NULL,
    net_salary NUMERIC NOT NULL,
    overtime_hours INTEGER DEFAULT 0,
    overtime_pay NUMERIC DEFAULT 0,
    leave_days INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT now(),
    UNIQUE(employee_id, month)
);

CREATE TABLE timesheets (
    timesheet_id SERIAL PRIMARY KEY,
    uploaded_by VARCHAR(10) REFERENCES employees(employee_id),
    month DATE NOT NULL,
    file_path VARCHAR(255),
    uploaded_at TIMESTAMP DEFAULT now()
);

-- Bảng chi tiết chấm công theo ngày cho từng nhân viên
CREATE TABLE attendance_details (
    attendance_id SERIAL PRIMARY KEY,
    employee_id VARCHAR(10) NOT NULL REFERENCES employees(employee_id),
    work_date DATE NOT NULL,
    check_in TIME,
    check_out TIME,
    work_type VARCHAR(30), -- ví dụ: 'Làm việc', 'Nghỉ phép', 'Làm thêm', ...
    note VARCHAR(255),
    created_at TIMESTAMP DEFAULT now(),
    UNIQUE(employee_id, work_date)
);
