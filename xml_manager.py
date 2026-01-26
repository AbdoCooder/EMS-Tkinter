
from lxml import etree
from db_manager import DataBaseManager
from validators import validate_employee_data

class xmlManager:
    def __init__(self) -> None:
        self.employee = {}

    def _extractDate(self, date_element):
        """Safely extract date from XML element, handling None values."""
        day = date_element[0].text or "01"
        month = date_element[1].text or "01"
        year = date_element[2].text or "2000"
        return f"{day}/{month}/{year}"

    def importXML(self, xml_file:str = "employes.xml"):
        if not self.validateXML(xml_file):
            raise Exception("The XML file" + xml_file + "doesn't match the DTD in employes.dtd")
        self.tree = etree.parse(xml_file)
        self.employes = self.tree.getroot()
        
        validation_errors = []
        imported_count = 0
        
        # Create single database connection for all imports
        db = DataBaseManager("employes.db")
        
        for idx, emp in enumerate(self.employes, start=1):
            identity = emp[0]
            full_name = identity[0].text
            birthday = self._extractDate(identity[1][0])
            hiring_date = self._extractDate(identity[2][0])
            departement = emp[1]
            dept_name = departement[0].text
            contact = emp[2]
            email = contact[0].text
            address = contact[1].text
            role = emp[3]
            job_title = role[0].text
            job_description = role[1].text
            self.employee = {
                "full_name":full_name,
                "birth_date":birthday,
                "hiring_date":hiring_date,
                "dept_name":dept_name,
                "email":email,
                "address":address,
                "job_title":job_title,
                "job_description":job_description
            }
            
            # Validate employee data before importing
            is_valid, errors = validate_employee_data(self.employee)
            if not is_valid:
                validation_errors.append(f"Employee #{idx} ({full_name or 'Unknown'}): {'; '.join(errors)}")
                continue
            
            db.add_employee(self.employee)
            imported_count += 1
        
        if validation_errors:
            error_msg = f"Imported {imported_count} employee(s). The following records had validation errors and were skipped:\n\n"
            error_msg += "\n\n".join(validation_errors)
            raise Exception(error_msg)


    def _exportIdentity(self, parent, dbRow):
        identity = etree.SubElement(parent, "identity")
        etree.SubElement(identity, "name").text = dbRow[1] # name

        birthday = etree.SubElement(identity, "birthday")
        self._exportDate(birthday, dbRow, 2)    # b_date

        hiring_date = etree.SubElement(identity, "hiring_date")
        self._exportDate(hiring_date, dbRow, 3) # h_date

    def _exportDate(self, parent, dbRow, dbCol):
        date = etree.SubElement(parent, "date")
        date_string = dbRow[dbCol]
        
        try:
            parts = date_string.split('/')
            if len(parts) == 3:
                day, month, year = parts
            else:
                day, month, year = "", "", "" 
        except (AttributeError, IndexError):
            day, month, year = "", "", ""
        etree.SubElement(date, "day").text = day
        etree.SubElement(date, "month").text = month
        etree.SubElement(date, "year").text = year

    def _exportDepartement(self, parent, dbRow):
        departement = etree.SubElement(parent, "departement")
        etree.SubElement(departement, "dept_name").text = dbRow[4]            # dept name

    def _exportContact(self, parent, dbRow):
        contact = etree.SubElement(parent, "contact")
        etree.SubElement(contact, "email").text = dbRow[5]                    # email
        etree.SubElement(contact, "address").text = dbRow[6]                  # address

    def _exportRole(self, parent, dbRow):
        role = etree.SubElement(parent, "role")
        etree.SubElement(role, "job_title").text = dbRow[7]                   # title
        etree.SubElement(role, "job_description").text = dbRow[8]             # description

    def exportXML(self, file:str="data.xml"):
        db = DataBaseManager("employes.db")
        dbEmp = db.get_employees()
        if dbEmp is None:
            dbEmp = []
        employes = etree.Element("employes")
        for emp in dbEmp:
            if len(emp) < 9:
                print(f"Skipping incomplete record: {emp}")
                continue
            employee = etree.SubElement(employes, "employee")
            self._exportIdentity(employee, emp)
            self._exportDepartement(employee, emp)
            self._exportContact(employee, emp)
            self._exportRole(employee, emp)

        tree = etree.ElementTree(employes)
        tree.write(file, pretty_print=True, xml_declaration=True, encoding="utf-8")

    def validateXML(self, xml_file: str = "data.xml", dtd_file: str = "employes.dtd"):
        try:
            dtd = etree.DTD(dtd_file)
            tree = etree.parse(xml_file)
            if dtd.validate(tree):
                print(f"✓ {xml_file} is valid against {dtd_file}")
                return True
            else:
                print(f"✗ {xml_file} is INVALID against {dtd_file}")
                print(f"Error log: {dtd.error_log}")
                return False
        except Exception as e:
            print(f"Error during validation: {e}")
            return False

# xml = xmlManager()
# xml.exportXML()
