import json
from flask import Blueprint, request
from dao import AddressDao
from models.Address import Address
from models.MyResponse import MyResponse

address_api = Blueprint("address_api", __name__)
dao = AddressDao


@address_api.route("/address", methods=["POST"])
def create_address():
    data = request.get_json()
    street = data.get("street")
    number = data.get("number")
    postcode = data.get("postcode")
    city = data.get("city")
    floor = data.get("floor")
    address = Address(address_id=-1, street=street, number=number, postcode=postcode, city=city, floor=floor)
    response = dao.create_address(address)
    return json.dumps(response.__dict__)


@address_api.route("/addresses", methods=["GET"])
def get_addresses():
    response = dao.fetch_addresses()
    if response.response_code == MyResponse.OK:
        addresses = response.response
        response_data = {
            "response": [address.__dict__ for address in addresses],
            "response_code": response.response_code
        }
        return json.dumps(response_data)
    else:
        return json.dumps(response.__dict__)


@address_api.route("/address/<int:address_id>", methods=["GET"])
def get_address_by_id(address_id):
    response = dao.get_address_by_id(address_id)
    if response.response_code == MyResponse.OK:
        address = response.response
        response_data = {
            "response": address.__dict__,
            "response_code": response.response_code
        }
        return json.dumps(response_data)
    elif response.response_code == MyResponse.NOT_FOUND:
        return json.dumps({
            "response": "Address not found",
            "response_code": response.response_code
        })
    else:
        return json.dumps({
            "response": "Something wrong happened, try again",
            "response_code": response.response_code
        })


@address_api.route("/address/<int:address_id>", methods=["PUT"])
def update_address(address_id):
    data = request.get_json()
    street = data.get("street")
    number = data.get("number")
    postcode = data.get("postcode")
    city = data.get("city")
    floor = data.get("floor")
    address = Address(address_id=address_id, street=street, number=number, postcode=postcode, city=city, floor=floor)
    response = dao.update_address(address)
    return json.dumps(response.__dict__)


@address_api.route("/address/<int:address_id>", methods=["DELETE"])
def delete_address(address_id):
    response = dao.delete_address(address_id)
    return json.dumps(response.__dict__)
