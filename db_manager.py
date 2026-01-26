import sqlite3

class DataBaseManager:
    def __init__(self, db_name: str = "employes.db", initialQuery=None) -> None:
        self.dbName = db_name
        if initialQuery:
            self.execdb(initialQuery)

    def execdb(self, query: str, parameters=(), fetch=False):
        con = None
        cur = None
        try:
            con = sqlite3.connect(self.dbName)
            cur = con.cursor()
            cur.execute(query, parameters)
            if fetch:
                return cur.fetchall()
            con.commit()
        except Exception as e:
            print(f"Error ❌: {e}")
            raise
        finally:
            if cur:
                cur.close()
            if con:
                con.close()

    def add_employee(self, data):
        query = """
        INSERT INTO employes (
            full_name, birth_date, hiring_date, 
            dept_name, email, address, 
            job_title, job_description
        ) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """

        values = (
            data["full_name"],
            data["birth_date"],
            data["hiring_date"],
            data["dept_name"],
            data["email"],
            data["address"],
            data["job_title"],
            data["job_description"],
        )

        self.execdb(query, values)

    def get_employees(self):
        query = "SELECT * FROM employes"
        return self.execdb(query, fetch=True)

    def delete_employee(self, employeeID):
        query = "DELETE FROM employes WHERE id = ?"
        self.execdb(query, (employeeID,))
    
    def update_employee(self, employeeID, data):
        query = """
        UPDATE employes SET
            full_name = ?,
            birth_date = ?,
            hiring_date = ?,
            dept_name = ?,
            email = ?,
            address = ?,
            job_title = ?,
            job_description = ?
        WHERE id = ?
        """
        
        values = (
            data["full_name"],
            data["birth_date"],
            data["hiring_date"],
            data["dept_name"],
            data["email"],
            data["address"],
            data["job_title"],
            data["job_description"],
            employeeID,
        )
        
        self.execdb(query, values)