import tkinter as tk
from db_manager import DataBaseManager
from ui_main import MainApp

# Database Configuration
DB_NAME = "employes.db"
INITIAL_QUERY = """CREATE TABLE IF NOT EXISTS employes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                birth_date TEXT,
                hiring_date TEXT,
                dept_name TEXT,
                email TEXT,
                address TEXT,
                job_title TEXT,
                job_description TEXT
             )"""

if __name__ == "__main__":
    # 1. Initialize DB (Create table if not exists)
    db = DataBaseManager(DB_NAME, INITIAL_QUERY)
    
    # 2. Launch GUI
    root = tk.Tk()
    root.minsize(width='1000', height='700')
    app = MainApp(root, db)
    root.mainloop()
