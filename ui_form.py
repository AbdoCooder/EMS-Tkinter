import tkinter as tk
from tkinter import ttk, messagebox

class EmployeeForm(tk.Toplevel):
    def __init__(self, parent, db, refresh_callback, employee_data=None):
        super().__init__(parent)
        self.db = db
        self.refresh_callback = refresh_callback
        self.employee_data = employee_data
        self.title("Employee Form")
        self.geometry("800x700")
        # self.resizable(False, False)
        self._build_ui()
        if self.employee_data:
            self._fill_fields()

    def _build_ui(self):
        frame_identity = tk.LabelFrame(self, text="Identity", padx=10, pady=10)
        frame_identity.pack(fill="x", padx=10, pady=5)
        tk.Label(frame_identity, text="Full Name:").grid(row=0, column=0, sticky="e")
        self.entry_name = tk.Entry(frame_identity, width=30)
        self.entry_name.grid(row=0, column=1, padx=5, pady=2)
        tk.Label(frame_identity, text="Birth Date (DD/MM/YYYY):").grid(row=0, column=2, sticky="e")
        self.entry_birth = tk.Entry(frame_identity, width=15)
        self.entry_birth.grid(row=0, column=3, padx=5, pady=2)
        tk.Label(frame_identity, text="Hiring Date (DD/MM/YYYY):").grid(row=1, column=0, sticky="e")
        self.entry_hiring = tk.Entry(frame_identity, width=15)
        self.entry_hiring.grid(row=1, column=1, sticky="w", padx=5, pady=2)

        frame_contact = tk.LabelFrame(self, text="Contact Info", padx=10, pady=10)
        frame_contact.pack(fill="x", padx=10, pady=5)
        tk.Label(frame_contact, text="Email:").grid(row=0, column=0, sticky="e")
        self.entry_email = tk.Entry(frame_contact, width=30)
        self.entry_email.grid(row=0, column=1, padx=5, pady=2)
        tk.Label(frame_contact, text="Address:").grid(row=1, column=0, sticky="e")
        self.entry_address = tk.Entry(frame_contact, width=40)
        self.entry_address.grid(row=1, column=1, columnspan=3, sticky="w", padx=5, pady=2)

        frame_job = tk.LabelFrame(self, text="Position", padx=10, pady=10)
        frame_job.pack(fill="x", padx=10, pady=5)
        tk.Label(frame_job, text="Department:").grid(row=0, column=0, sticky="e")
        self.combo_dept = ttk.Combobox(frame_job, values=["IT", "HR", "Finance", "Marketing"], width=27)
        self.combo_dept.grid(row=0, column=1, padx=5, pady=2)
        tk.Label(frame_job, text="Job Title:").grid(row=1, column=0, sticky="e")
        self.entry_title = tk.Entry(frame_job, width=30)
        self.entry_title.grid(row=1, column=1, padx=5, pady=2)
        tk.Label(frame_job, text="Description:").grid(row=2, column=0, sticky="ne")
        self.entry_desc = tk.Text(frame_job, width=30, height=3)
        self.entry_desc.grid(row=2, column=1, padx=5, pady=2)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Save", bg="#4CAF50", fg="white", width=15, command=self.save_employee).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Cancel", width=15, command=self.destroy).pack(side="left", padx=10)

    def _fill_fields(self):
        if not self.employee_data:
            return
        d = self.employee_data
        self.entry_name.insert(0, d[1])
        self.entry_birth.insert(0, d[2])
        self.entry_hiring.insert(0, d[3])
        self.combo_dept.set(d[4])
        self.entry_email.insert(0, d[5])
        self.entry_address.insert(0, d[6])
        self.entry_title.insert(0, d[7])
        self.entry_desc.insert("1.0", d[8])

    def _validate_date_format(self, date_string):
        """Validate date format DD/MM/YYYY"""
        if not date_string:
            return True
        try:
            parts = date_string.split('/')
            if len(parts) != 3:
                return False
            day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
            if day < 1 or day > 31 or month < 1 or month > 12 or year < 1900:
                return False
            return True
        except ValueError:
            return False

    def save_employee(self):
        data = {
            "full_name": self.entry_name.get(),
            "birth_date": self._validate_date_format(self.entry_birth.get()) and self.entry_birth.get() or None,
            "hiring_date": self._validate_date_format(self.entry_hiring.get()) and self.entry_hiring.get() or None,
            "dept_name": self.combo_dept.get() or None,
            "email": self.entry_email.get() or None,
            "address": self.entry_address.get() or None,
            "job_title": self.entry_title.get() or None,
            "job_description": self.entry_desc.get("1.0", "end-1c") or None,
        }
        if not data["full_name"] or not data["dept_name"]:
            self.refresh_callback()
            self.destroy()
            messagebox.showerror("Error", "Name and Department are required!")
            return
        try:
            if self.employee_data:
                self.db.update_employee(self.employee_data[0], data)
                self.refresh_callback()
                self.destroy()
                messagebox.showinfo("Success", "Employee updated successfully!")
            else:
                self.db.add_employee(data)
                self.refresh_callback()
                self.destroy()
                messagebox.showinfo("Success", "Employee added successfully!")
        except Exception as e:
            self.refresh_callback()
            self.destroy()
            messagebox.showerror("Database Error", str(e))
