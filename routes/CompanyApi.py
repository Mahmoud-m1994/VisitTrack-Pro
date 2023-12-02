import json
from flask import Blueprint, request
from dao import CompanyDao
from models.Address import Address
from models.MyResponse import MyResponse
from models.Company import Company

company_api = Blueprint("company_api", __name__)
dao = CompanyDao


@company_api.route("/companies", methods=["POST"])
def create_company_endpoint():
    data = request.get_json()
    name = data.get("name")

    address = None
    if data.get("address") is not None:
        address_data = data.get("address")
        street = address_data.get("street")
        number = address_data.get("number")
        postcode = address_data.get("postcode")
        city = address_data.get("city")
        floor = address_data.get("floor")

        address = Address(address_id=-1, street=street, number=number, postcode=postcode, city=city, floor=floor)

    company = Company(company_id=-1, name=name, address_id=-1)

    response = dao.create_company(company, address)

    return json.dumps(response.__dict__)


@company_api.route("/companies", methods=["GET"])
def fetch_companies_endpoint():
    response = dao.fetch_all_companies()

    if response.response_code == MyResponse.OK:
        companies = response.response
        response_data = {
            "response": [company.__dict__ for company in companies],
            "response_code": response.response_code
        }
        return json.dumps(response_data)
    else:
        return json.dumps(response.__dict__)


@company_api.route("/company/<int:company_id>", methods=["GET"])
def get_company_by_id_endpoint(company_id):
    response = dao.get_company_by_id(company_id)

    if response.response_code == MyResponse.OK:
        company = response.response
        response_data = {
            "response": company.__dict__,
            "response_code": response.response_code
        }
        return json.dumps(response_data)
    elif response.response_code == MyResponse.NOT_FOUND:
        return json.dumps({
            "response": "Company not found",
            "response_code": response.response_code
        })
    else:
        return json.dumps({
            "response": "Something wrong happened, try again",
            "response_code": response.response_code
        })


@company_api.route("/company/<int:company_id>", methods=["PUT"])
def update_company_endpoint(company_id):
    data = request.get_json()
    name = data.get("name")
    company = Company(company_id=company_id, name=name, address_id=-1)

    response = dao.update_company(company)

    return json.dumps(response.__dict__)


@company_api.route("/company/<int:company_id>", methods=["DELETE"])
def delete_company_endpoint(company_id):
    response = dao.delete_company(company_id)
    return json.dumps(response.__dict__)
