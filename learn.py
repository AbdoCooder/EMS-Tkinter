import tkinter as tk
from db_manager import DataBaseManager

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


def shownames():
    list.delete(0, tk.END)
    emps = db.get_employees()
    for e in emps:
        list.insert(tk.END, e)

db = DataBaseManager(DB_NAME, INITIAL_QUERY)
root = tk.Tk()
root.geometry('1920x1080')
list = tk.Listbox(root)
btn = tk.Button(root, text='Load Data', command=shownames)
btn.grid(row=0, column=0, sticky=(tk.NSEW))
list.grid(row=3, column=0)
root.mainloop()
