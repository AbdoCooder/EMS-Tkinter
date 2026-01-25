import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# import DB layer
from db_manager import (
    init_db,
    fetch_employees,
    fetch_departments,
    insert_employee,
    update_employee,
    delete_employee
)


class EmployeeApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("EMS - Employee Management System")
        self.geometry("1200x650")
        self.minsize(1100, 600)

        self.selected_id = None

        self.build_ui()
        self.refresh_table()

    # ================= UI =================
    def build_ui(self):
        # ---- Top bar
        top = ttk.Frame(self, padding=10)
        top.pack(fill="x")

        ttk.Label(top, text="Search:").pack(side="left")
        self.search_var = tk.StringVar()
        ttk.Entry(top, textvariable=self.search_var, width=35).pack(side="left", padx=(5, 15))
        self.search_var.trace_add("write", lambda *args: self.refresh_table())

        ttk.Label(top, text="Department:").pack(side="left")
        self.dept_var = tk.StringVar(value="All")
        self.dept_combo = ttk.Combobox(top, textvariable=self.dept_var, state="readonly", width=18)
        self.dept_combo.pack(side="left", padx=(5, 15))
        self.dept_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_table())

        ttk.Button(top, text="Clear Form", command=self.clear_form).pack(side="right")

        # ---- Body
        body = ttk.Frame(self, padding=(10, 0, 10, 10))
        body.pack(fill="both", expand=True)

        # ---- Table
        left = ttk.Frame(body)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))
        self.build_table(left)

        # ---- Form
        right = ttk.LabelFrame(body, text="Employee Form", padding=10)
        right.pack(side="right", fill="y")
        self.build_form(right)

    def build_table(self, parent):
        columns = (
            "id", "name", "birth_date", "hiring_date",
            "dept_name", "email", "address",
            "job_title", "job_description"
        )

        self.tree = ttk.Treeview(parent, columns=columns, show="headings")
        self.tree.pack(fill="both", expand=True)

        headers = {
            "id": "ID",
            "name": "Name",
            "birth_date": "Birth Date",
            "hiring_date": "Hiring Date",
            "dept_name": "Department",
            "email": "Email",
            "address": "Address",
            "job_title": "Job Title",
            "job_description": "Job Description",
        }

        for col in columns:
            self.tree.heading(col, text=headers[col])
            self.tree.column(col, width=140)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def build_form(self, parent):
        self.name_var = tk.StringVar()
        self.birth_var = tk.StringVar()
        self.hiring_var = tk.StringVar()
        self.dept_form_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.job_title_var = tk.StringVar()

        fields = [
            ("Name *", self.name_var),
            ("Birth Date (YYYY-MM-DD)", self.birth_var),
            ("Hiring Date (YYYY-MM-DD)", self.hiring_var),
            ("Department", self.dept_form_var),
            ("Email", self.email_var),
            ("Address", self.address_var),
            ("Job Title", self.job_title_var),
        ]

        for i, (label, var) in enumerate(fields):
            ttk.Label(parent, text=label).grid(row=i, column=0, sticky="w", pady=4)
            ttk.Entry(parent, textvariable=var, width=32, style="Form.TEntry")\
                .grid(row=i, column=1, pady=4)

        ttk.Label(parent, text="Job Description").grid(row=7, column=0, sticky="nw")
        self.job_desc = tk.Text(parent, width=30, height=5, relief="solid", bd=1)
        self.job_desc.grid(row=7, column=1, pady=4)

        # Buttons
        btns = ttk.Frame(parent)
        btns.grid(row=8, column=0, columnspan=2, pady=15)

        ttk.Button(btns, text="Add", command=self.add_employee).pack(side="left", padx=5)
        ttk.Button(btns, text="Update", command=self.update_employee).pack(side="left", padx=5)
        ttk.Button(btns, text="Delete", command=self.delete_employee).pack(side="left", padx=5)

    # ================= LOGIC =================
    def refresh_table(self):
        self.dept_combo["values"] = fetch_departments()

        for i in self.tree.get_children():
            self.tree.delete(i)

        rows = fetch_employees(self.search_var.get(), self.dept_var.get())
        for r in rows:
            self.tree.insert("", "end", values=r)

    def read_form(self):
        return {
            "name": self.name_var.get().strip(),
            "birth_date": self.birth_var.get().strip(),
            "hiring_date": self.hiring_var.get().strip(),
            "dept_name": self.dept_form_var.get().strip(),
            "email": self.email_var.get().strip(),
            "address": self.address_var.get().strip(),
            "job_title": self.job_title_var.get().strip(),
            "job_description": self.job_desc.get("1.0", "end").strip(),
        }

    def clear_form(self):
        self.selected_id = None
        for var in [
            self.name_var, self.birth_var, self.hiring_var,
            self.dept_form_var, self.email_var,
            self.address_var, self.job_title_var
        ]:
            var.set("")
        self.job_desc.delete("1.0", "end")

    def on_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return

        values = self.tree.item(sel[0], "values")
        self.selected_id = int(values[0])

        self.name_var.set(values[1])
        self.birth_var.set(values[2])
        self.hiring_var.set(values[3])
        self.dept_form_var.set(values[4])
        self.email_var.set(values[5])
        self.address_var.set(values[6])
        self.job_title_var.set(values[7])
        self.job_desc.delete("1.0", "end")
        self.job_desc.insert("1.0", values[8])

    def add_employee(self):
        data = self.read_form()
        if not data["name"]:
            messagebox.showerror("Erreur", "Name est obligatoire")
            return
        insert_employee(data)
        self.refresh_table()
        self.clear_form()

    def update_employee(self):
        if self.selected_id is None:
            messagebox.showwarning("Attention", "Sélectionne un employé")
            return
        update_employee(self.selected_id, self.read_form())
        self.refresh_table()
        self.clear_form()

    def delete_employee(self):
        if self.selected_id is None:
            return
        if messagebox.askyesno("Confirmation", "Supprimer cet employé ?"):
            delete_employee(self.selected_id)
            self.refresh_table()
            self.clear_form()


# ================= RUN =================
if __name__ == "__main__":
    init_db()
    app = EmployeeApp()
    app.mainloop()
