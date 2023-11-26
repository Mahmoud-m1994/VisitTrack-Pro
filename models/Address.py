class Address:
    def __init__(self, address_id, street, number, postcode, city, floor=None):
        self.address_id = address_id
        self.street = street
        self.number = number
        self.postcode = postcode
        self.city = city
        self.floor = floor
