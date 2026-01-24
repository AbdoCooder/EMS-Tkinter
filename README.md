# 📂 Employee Management System (EMS)

A desktop application for managing employees, built with **Python (Tkinter)** and **SQLite3**, featuring XML data import/export.

## 🚀 Getting Started

### Prerequisites
- **Python 3.x** installed
- **lxml** library for XML processing with DTD validation

Install dependencies:
```bash
pip install lxml
```

Standard libraries used: `sqlite3`, `tkinter`

### How to Run
The backend (Database + XML Manager) is fully functional. You can test:

**Database Operations:**
```bash
python db_manager.py
```

**XML Import/Export:**
```python
from xml_manager import xmlManager
xml = xmlManager()
xml.importXML("employes.xml")  # Import employees from XML
xml.exportXML("output.xml")     # Export employees to XML
```

## 🏗️ Project Structure & Responsibilities

To avoid code conflicts, we have separated the logic (Backend) from the interface (Frontend).

| File | Description | Responsibility |
|------|-------------|----------------|
| `db_manager.py` | Handles SQLite connection and CRUD operations.  | Backend ✅ |
| `xml_manager.py` | XML Import/Export with DTD validation. | Backend ✅ |
| `employes.dtd` | Defines the XML structure we must respect.  | Shared |
| `ui_main.py` | The main Tkinter window (Treeview, Search, Buttons). | Frontend (To-Do) |
| `ui_form.py` | Pop-up windows for Adding/Editing employees. | Frontend (To-Do) |
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
    "full_name": "Ahmed Alami",
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

#### ➤ Update an Employee

Pass the employee ID and a dictionary with updated data.

```python
updated_emp = {
    "full_name": "Ahmed Alami",
    "birth_date": "1990-01-01",
    "hiring_date":  "2023-05-12",
    "dept_name": "DevOps",
    "email": "ahmed.alami@test.com",
    "address": "Tetouan",
    "job_title":  "Senior Developer",
    "job_description": "Full Stack Dev"
}

db.update_employee(emp_id, updated_emp)
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
- **DTD Validation:** XML files are validated against `employes.dtd` before import to ensure data integrity.

### Database Schema

The table `employes` has the following columns:

| Column | Description |
|--------|-------------|
| `id` | Auto-increment primary key |
| `full_name` | Employee's full name |
| `birth_date` | Date of birth (format: DD/MM/YYYY) |
| `hiring_date` | Date of hiring (format: DD/MM/YYYY) |
| `dept_name` | Department name |
| `email` | Email address |
| `address` | Physical address |
| `job_title` | Job title |
| `job_description` | Job description |

## 🔄 XML Manager Documentation

The `xml_manager.py` module provides full XML import/export capabilities with DTD validation.

### Import from XML

```python
from xml_manager import xmlManager

xml = xmlManager()
xml.importXML("employes.xml")  # Validates and imports employees
```

**Features:**
- Automatic DTD validation before import
- Parses hierarchical XML structure (identity, department, contact, role)
- Converts date format from XML to database format
- Prevents invalid data through DTD schema enforcement

### Export to XML

```python
from xml_manager import xmlManager

xml = xmlManager()
xml.exportXML("output.xml")  # Exports all employees from database
```

**Features:**
- Exports all employees from database to XML
- Maintains DTD-compliant structure
- Pretty-printed, UTF-8 encoded output
- Includes XML declaration

### Validate XML

```python
from xml_manager import xmlManager

xml = xmlManager()
is_valid = xml.validateXML("employes.xml", "employes.dtd")
```

Returns `True` if XML is valid, `False` otherwise with error details.

## ✅ To-Do List

- [x] Create Database Manager & CRUD (Backend)
- [x] Define DTD Structure
- [x] Implement XML Manager with DTD Validation
- [x] Implement XML Export/Import logic
- [x] Add Update Employee functionality
- [ ] Build Main Window (Treeview + Search)
- [ ] Build "Add Employee" Form
- [ ] Build "Edit Employee" Form
- [ ] Connect Frontend Buttons to Backend Functions
