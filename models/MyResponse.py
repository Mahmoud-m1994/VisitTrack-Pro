class MyResponse:
    OK = 200
    ERROR = 500
    NOT_FOUND = 404
    ALREADY_EXISTING = 409
    CREATED = 201
    UNAUTHORIZED = 401
    BAD_REQUEST = 400

    def __init__(self, response, response_code: int):
        self.response = response
        self.response_code = response_code
