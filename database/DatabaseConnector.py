import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

host = os.getenv('HOST')
user = os.getenv('USER')
password = os.getenv('PASSWORD')
database = os.getenv('DATABASE')
port = os.getenv('PORT')


def connect_to_mysql():
    try:
        print("Host:", host)
        print("Username:", user)
        print("Password:", password)
        print("Database:", database)
        print("Port:", port)

        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,
        )
        print("Connected to MySQL database")
        return connection
    except mysql.connector.Error as err:
        print("Error connecting to MySQL database:", err)
        return None


def disconnect_from_mysql(connection):
    if connection:
        connection.close()
        print("Disconnected from MySQL database")
    else:
        print("Connection is null")