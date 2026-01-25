import sqlite3

DB_PATH = "employeesDB.db"

def get_conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                birth_date TEXT,
                hiring_date TEXT,
                dept_name TEXT,
                email TEXT,
                address TEXT,
                job_title TEXT,
                job_description TEXT
            )
        """)
        conn.commit()

def fetch_employees(search_text="", dept_filter="All"):
    search_text = (search_text or "").strip()
    with get_conn() as conn:
        cur = conn.cursor()

        base_query = """
            SELECT id, name, birth_date, hiring_date, dept_name, email, address, job_title, job_description
            FROM employees
        """
        conditions = []
        params = []

        if search_text:
            conditions.append("(name LIKE ? OR email LIKE ? OR job_title LIKE ? OR dept_name LIKE ?)")
            like = f"%{search_text}%"
            params.extend([like, like, like, like])

        if dept_filter and dept_filter != "All":
            conditions.append("dept_name = ?")
            params.append(dept_filter)

        if conditions:
            base_query += " WHERE " + " AND ".join(conditions)

        base_query += " ORDER BY id DESC"

        cur.execute(base_query, params)
        return cur.fetchall()

def insert_employee(data: dict):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO employees
            (name, birth_date, hiring_date, dept_name, email, address, job_title, job_description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["name"], data["birth_date"], data["hiring_date"], data["dept_name"],
            data["email"], data["address"], data["job_title"], data["job_description"]
        ))
        conn.commit()

def update_employee(emp_id: int, data: dict):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE employees
            SET name = ?, birth_date = ?, hiring_date = ?, dept_name = ?, email = ?, address = ?, job_title = ?, job_description = ?
            WHERE id = ?
        """, (
            data["name"], data["birth_date"], data["hiring_date"], data["dept_name"],
            data["email"], data["address"], data["job_title"], data["job_description"],
            emp_id
        ))
        conn.commit()

def delete_employee(emp_id: int):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM employees WHERE id = ?", (emp_id,))
        conn.commit()

def fetch_departments():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT dept_name
            FROM employees
            WHERE dept_name IS NOT NULL AND dept_name != ''
            ORDER BY dept_name
        """)
        depts = [r[0] for r in cur.fetchall()]
        return ["All"] + depts
