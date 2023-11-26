from flask import Flask
from routes.AddressApi import address_api

app = Flask(__name__)
app.register_blueprint(address_api)

if __name__ == '__main__':
    print('Hey from Task tracking server')
    app.run()
