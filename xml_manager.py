
from lxml import etree
from db_manager import DataBaseManager

class xmlManager:
    def __init__(self) -> None:
        self.employee = {}

    def importXML(self, xml_file:str = "employes.xml"):
        self.tree = etree.parse(xml_file)
        self.employes = self.tree.getroot()
        for emp in self.employes:
            identity = emp[0]
            full_name = identity[0].text
            birthday = identity[1][0][0].text + '/' + identity[1][0][1].text + '/' + identity[1][0][2].text
            hiring_date = identity[2][0][0].text + '/' + identity[2][0][1].text + '/' + identity[2][0][2].text
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
            db = DataBaseManager("employes.db")
            db.add_employee(self.employee)


    def exportXML(self):
        db = DataBaseManager("employes.db")
        db.get_employees()


xml = xmlManager()
xml.importXML()
