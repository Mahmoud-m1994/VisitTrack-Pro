class Employee:
    def __init__(self, employee_id, name, mail, phone, address_id=None):
        self.employee_id = employee_id
        self.name = name
        self.mail = mail
        self.phone = phone
        self.address_id = address_id
