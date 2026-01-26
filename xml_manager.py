from lxml import etree
from db_manager import DataBaseManager

class xmlManager:
    def _extractDate(self, date_element):
        day = date_element[0].text or "01"
        month = date_element[1].text or "01"
        year = date_element[2].text or "2000"
        return f"{day}/{month}/{year}"

    def importXML(self, xml_file: str = "employes.xml"):
        if not self.validateXML(xml_file):
            raise Exception(f"XML file {xml_file} doesn't match DTD")
        tree = etree.parse(xml_file)
        db = DataBaseManager("employes.db")
        for emp in tree.getroot():
            identity, dept, contact, role = emp[0], emp[1], emp[2], emp[3]
            db.add_employee({
                "full_name": identity[0].text,
                "birth_date": self._extractDate(identity[1][0]),
                "hiring_date": self._extractDate(identity[2][0]),
                "dept_name": dept[0].text,
                "email": contact[0].text,
                "address": contact[1].text,
                "job_title": role[0].text,
                "job_description": role[1].text
            })

    def _exportDate(self, parent, date_string):
        date = etree.SubElement(parent, "date")
        try:
            parts = date_string.split('/') if date_string else []
            day, month, year = (parts + ["", "", ""])[:3]
        except (AttributeError, IndexError):
            day, month, year = "", "", ""
        etree.SubElement(date, "day").text = day
        etree.SubElement(date, "month").text = month
        etree.SubElement(date, "year").text = year

    def exportXML(self, file: str = "data.xml"):
        db = DataBaseManager("employes.db")
        dbEmp = db.get_employees() or []
        employes = etree.Element("employes")
        for emp in dbEmp:
            if len(emp) < 9:
                continue
            employee = etree.SubElement(employes, "employee")
            identity = etree.SubElement(employee, "identity")
            etree.SubElement(identity, "name").text = emp[1]
            birthday = etree.SubElement(identity, "birthday")
            self._exportDate(birthday, emp[2])
            hiring = etree.SubElement(identity, "hiring_date")
            self._exportDate(hiring, emp[3])
            dept = etree.SubElement(employee, "departement")
            etree.SubElement(dept, "dept_name").text = emp[4]
            contact = etree.SubElement(employee, "contact")
            etree.SubElement(contact, "email").text = emp[5]
            etree.SubElement(contact, "address").text = emp[6]
            role = etree.SubElement(employee, "role")
            etree.SubElement(role, "job_title").text = emp[7]
            etree.SubElement(role, "job_description").text = emp[8]
        etree.ElementTree(employes).write(file, pretty_print=True, xml_declaration=True, encoding="utf-8")

    def validateXML(self, xml_file: str = "data.xml", dtd_file: str = "employes.dtd"):
        try:
            dtd = etree.DTD(dtd_file)
            return dtd.validate(etree.parse(xml_file))
        except Exception:
            return False
