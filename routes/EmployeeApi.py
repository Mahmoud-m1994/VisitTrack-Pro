import json
from flask import Blueprint, request
from dao import EmployeeDao
from models.Address import Address
from models.MyResponse import MyResponse
from models.Employee import Employee

employee_api = Blueprint("employee_api", __name__)
dao = EmployeeDao


@employee_api.route("/employees", methods=["POST"])
def create_employee_endpoint():
    data = request.get_json()
    name = data.get("name")
    mail = data.get("mail")
    phone = data.get("phone")

    address = None
    if data.get("address") is not None:
        address_data = data.get("address")
        street = address_data.get("street")
        number = address_data.get("number")
        postcode = address_data.get("postcode")
        city = address_data.get("city")
        floor = address_data.get("floor")

        address = Address(address_id=-1, street=street, number=number, postcode=postcode, city=city, floor=floor)

    employee = Employee(employee_id=-1, name=name, mail=mail, phone=phone, address_id=-1)

    response = dao.create_employee(employee, address)

    return json.dumps(response.__dict__)


@employee_api.route("/employees", methods=["GET"])
def fetch_employees_endpoint():
    response = dao.fetch_employees()

    if response.response_code == MyResponse.OK:
        employees = response.response
        response_data = {
            "response": [employee.__dict__ for employee in employees],
            "response_code": response.response_code
        }
        return json.dumps(response_data)
    else:
        return json.dumps(response.__dict__)


@employee_api.route("/employee/<int:employee_id>", methods=["GET"])
def get_employee_by_id_endpoint(employee_id):
    response = dao.get_employee_by_id(employee_id)

    if response.response_code == MyResponse.OK:
        employee = response.response
        response_data = {
            "response": employee.__dict__,
            "response_code": response.response_code
        }
        return json.dumps(response_data)
    elif response.response_code == MyResponse.NOT_FOUND:
        return json.dumps({
            "response": "employee not found",
            "response_code": response.response_code
        })
    else:
        return json.dumps({
            "response": "Something wrong happened, try again",
            "response_code": response.response_code
        })


@employee_api.route("/employee/<int:employee_id>", methods=["PUT"])
def update_employee_endpoint(employee_id):
    data = request.get_json()
    name = data.get("name")
    mail = data.get("mail")
    phone = data.get("phone")
    employee = Employee(employee_id=employee_id, name=name, mail=mail, phone=phone, address_id=-1)

    response = dao.update_employee(employee)

    return json.dumps(response.__dict__)


@employee_api.route("/employee/<int:employee_id>", methods=["DELETE"])
def delete_employee_endpoint(employee_id):
    response = dao.delete_employee(employee_id)
    return json.dumps(response.__dict__)
