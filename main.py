from flask import Flask
from routes.AddressApi import address_api
from routes.EmployeeApi import employee_api
from routes.CompanyApi import company_api

app = Flask(__name__)
app.register_blueprint(address_api)
app.register_blueprint(employee_api)
app.register_blueprint(company_api)

if __name__ == '__main__':
    print('Hey from Task tracking server')
    app.run(host='0.0.0.0', port=5000)
