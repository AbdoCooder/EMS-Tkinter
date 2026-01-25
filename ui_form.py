import tkinter as tk
from tkinter import ttk, messagebox

class EmployeeForm(tk.Toplevel):
    def __init__(self, parent, db, refresh_callback, employee_data=None):
        super().__init__(parent)
        self.db = db
        self.refresh_callback = refresh_callback
        self.employee_data = employee_data # If not None, we are in "Edit Mode"
        
        self.title("Employee Form")
        self.geometry("600x550")
        self.resizable(False, False)

        self._build_ui()

        # If editing, fill fields
        if self.employee_data:
            self._fill_fields()

    def _build_ui(self):
        # --- Section 1: Identity ---
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

        # --- Section 2: Contact ---
        frame_contact = tk.LabelFrame(self, text="Contact Info", padx=10, pady=10)
        frame_contact.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_contact, text="Email:").grid(row=0, column=0, sticky="e")
        self.entry_email = tk.Entry(frame_contact, width=30)
        self.entry_email.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(frame_contact, text="Address:").grid(row=1, column=0, sticky="e")
        self.entry_address = tk.Entry(frame_contact, width=40)
        self.entry_address.grid(row=1, column=1, columnspan=3, sticky="w", padx=5, pady=2)

        # --- Section 3: Job Position ---
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

        # --- Buttons ---
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Save", bg="#4CAF50", fg="white", width=15, command=self.save_employee).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Cancel", width=15, command=self.destroy).pack(side="left", padx=10)

    def _fill_fields(self):
        # Mapping tuple data (from Treeview) to inputs
        # Tuple: (id, name, birth, hiring, dept, email, address, title, desc)
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

    def save_employee(self):
        # 1. Collect Data
        data = {
            "full_name": self.entry_name.get(),
            "birth_date": self.entry_birth.get(),
            "hiring_date": self.entry_hiring.get(),
            "dept_name": self.combo_dept.get(),
            "email": self.entry_email.get(),
            "address": self.entry_address.get(),
            "job_title": self.entry_title.get(),
            "job_description": self.entry_desc.get("1.0", "end-1c")
        }

        # 2. Basic Validation
        if not data["full_name"] or not data["dept_name"]:
            messagebox.showerror("Error", "Name and Department are required!")
            return

        try:
            if self.employee_data:
                # Update Mode (Pass ID)
                emp_id = self.employee_data[0]
                self.db.update_employee(emp_id, data)
                messagebox.showinfo("Success", "Employee updated successfully!")
            else:
                # Add Mode
                self.db.add_employee(data)
                messagebox.showinfo("Success", "Employee added successfully!")
            
            self.refresh_callback() # Refresh Main Table
            self.destroy() # Close window
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
