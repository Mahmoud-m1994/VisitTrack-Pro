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
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,
        )
        return connection
    except mysql.connector.Error as err:
        print("Error connecting to MySQL database:", err)
        return None


def disconnect_from_mysql(connection):
    if connection:
        connection.close()
    else:
        print("Connection is null")