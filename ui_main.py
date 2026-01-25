import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from ui_form import EmployeeForm
from xml_manager import xmlManager

class MainApp:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.xml_mgr = xmlManager()

        self.root.title("Employee Management System")
        self.root.geometry("1000x600")

        self._setup_menu()
        self._setup_filters()
        self._setup_treeview()
        self._setup_buttons()

        self.load_data()

    def _setup_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Import XML...", command=self.import_xml)
        file_menu.add_command(label="Export XML...", command=self.export_xml)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menubar)

    def _setup_filters(self):
        frame_top = tk.Frame(self.root, bg="#f0f0f0", pady=10)
        frame_top.pack(fill="x")

        tk.Label(frame_top, text="Search Name:", bg="#f0f0f0").pack(side="left", padx=10)
        self.search_var = tk.StringVar()
        entry_search = tk.Entry(frame_top, textvariable=self.search_var)
        entry_search.pack(side="left", padx=5)
        
        tk.Button(frame_top, text="🔍 Search", command=self.filter_data).pack(side="left", padx=5)
        tk.Button(frame_top, text="🔄 Reset", command=self.load_data).pack(side="left", padx=5)

    def _setup_treeview(self):
        # Columns must match DB SELECT order
        # ID, Name, Birth, Hiring, Dept, Email, Address, Title, Desc
        cols = ("ID", "Name", "Birth Date", "Hiring Date", "Dept", "Email", "Address", "Title", "Desc")
        
        self.tree = ttk.Treeview(self.root, columns=cols, show="headings")
        
        # Configure Headers and Widths
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Special width for ID and Desc
        self.tree.column("ID", width=30)
        self.tree.column("Desc", width=150)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

    def _setup_buttons(self):
        frame_btn = tk.Frame(self.root, pady=10)
        frame_btn.pack(fill="x")

        tk.Button(frame_btn, text="➕ Add Employee", bg="#2196F3", fg="white", font=("Arial", 10, "bold"), 
                  command=self.open_add_form).pack(side="left", padx=20)
        
        tk.Button(frame_btn, text="✏️ Edit Selected", bg="#FFC107", 
                  command=self.open_edit_form).pack(side="left", padx=20)
        
        tk.Button(frame_btn, text="❌ Delete Selected", bg="#F44336", fg="white", 
                  command=self.delete_employee).pack(side="right", padx=20)

    # --- Data Logic ---
    def load_data(self):
        # Clear Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fetch from DB
        rows = self.db.get_employees()
        for row in rows:
            self.tree.insert("", "end", values=row)

    def filter_data(self):
        keyword = self.search_var.get().lower()
        if not keyword:
            return

        # Simple client-side filter (can be moved to SQL for optimization)
        rows = self.db.get_employees()
        filtered = [row for row in rows if keyword in row[1].lower() or keyword in row[4].lower()]
        
        # Clear and Refill
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in filtered:
            self.tree.insert("", "end", values=row)

    # --- Actions ---
    def open_add_form(self):
        EmployeeForm(self.root, self.db, self.load_data)

    def open_edit_form(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an employee to edit")
            return
        
        # Get data from Treeview
        item = self.tree.item(selected[0])
        data = item['values'] # This is the tuple (id, name, ...)
        
        EmployeeForm(self.root, self.db, self.load_data, employee_data=data)

    def delete_employee(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select an employee to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this employee?"):
            item_id = self.tree.item(selected[0])['values'][0] # ID is at index 0
            self.db.delete_employee(item_id)
            self.load_data()

    # --- XML Integration ---
    def import_xml(self):
        filename = filedialog.askopenfilename(filetypes=[("XML Files", "*.xml")])
        if filename:
            try:
                self.xml_mgr.importXML(filename)
                self.load_data()
                messagebox.showinfo("Success", "XML Imported successfully!")
            except Exception as e:
                messagebox.showerror("XML Error", str(e))

    def export_xml(self):
        filename = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML Files", "*.xml")])
        if filename:
            try:
                self.xml_mgr.exportXML(filename)
                messagebox.showinfo("Success", "Data exported to XML!")
            except Exception as e:
                messagebox.showerror("XML Error", str(e))
