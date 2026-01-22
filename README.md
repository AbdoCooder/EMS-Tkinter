# 📂 Employee Management System (EMS)

A desktop application for managing employees, built with **Python (Tkinter)** and **SQLite3**, featuring XML data import/export.

## 🚀 Getting Started

### Prerequisites
You only need Python installed. No external libraries are required (we use standard libraries: `sqlite3`, `tkinter`, `xml`).

### How to Run
Currently, the backend is ready. You can test the database creation by running:

```bash
python db_manager.py
```

## 🏗️ Project Structure & Responsibilities

To avoid code conflicts, we have separated the logic (Backend) from the interface (Frontend).

| File | Description | Responsibility |
|------|-------------|----------------|
| `db_manager.py` | Handles SQLite connection and CRUD operations.  | Backend (Me) |
| `employes.dtd` | Defines the XML structure we must respect.  | Shared |
| `ui_main.py` | The main Tkinter window (Treeview, Search, Buttons). | Frontend (You) |
| `ui_form.py` | Pop-up windows for Adding/Editing employees. | Frontend (You) |
| `main.py` | Entry point that launches the application.  | Shared |

## 🛠️ Backend Documentation (For Frontend Integration)

I have created a `db` object in `db_manager.py` that you can import into your Tkinter files.

### 1. How to Import the Database

In your UI file (`ui_main.py` or `main.py`), add this line: 

```python
from db_manager import db
```

### 2. Available Methods

Use these methods to interact with the data. You don't need to write any SQL queries.

#### ➤ Get All Employees (For the Treeview)

Returns a list of tuples. 

```python
employees = db.get_employees()
# Loop through 'employees' to insert into your Treeview
```

#### ➤ Add a New Employee

Pass a dictionary with exact keys matching the form fields.

```python
new_emp = {
    "name": "Ahmed Alami",
    "birth_date": "1990-01-01",
    "hiring_date":  "2023-05-12",
    "dept_name": "IT",
    "email": "ahmed@test.com",
    "address": "Tetouan",
    "job_title":  "Developer",
    "job_description": "Python Dev"
}

db.add_employee(new_emp)
```

#### ➤ Delete an Employee

Pass the ID (hidden column in your Treeview).

```python
db.delete_employee(emp_id)
```

## 📜 Data Rules (DTD & Schema)

### XML Logic

We agreed that XML Import acts as a "New Registration" form. 

- **No IDs in XML:** The DTD does not strictly require an ID.
- **Auto-Increment:** When we import XML, SQLite automatically assigns a new ID to avoid duplicates/conflicts. 

### Database Schema

The table `employes` has the following columns:

| Column | Description |
|--------|-------------|
| `id` | Auto-increment primary key |
| `full_name` | Employee's full name |
| `birth_date` | Date of birth |
| `hiring_date` | Date of hiring |
| `dept_name` | Department name |
| `email` | Email address |
| `address` | Physical address |
| `job_title` | Job title |
| `job_description` | Job description |

## ✅ To-Do List

- [x] Create Database Manager & CRUD (Backend)
- [x] Define DTD Structure
- [ ] Build Main Window (Treeview + Search)
- [ ] Build "Add Employee" Form
- [ ] Connect Frontend Buttons to Backend Functions
- [ ] Implement XML Export/Import logic
