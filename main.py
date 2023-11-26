# main.py
from database.DatabaseConnector import connect_to_mysql, disconnect_from_mysql

if __name__ == '__main__':
    print('Hey from Task tracking server')
    connect_to_mysql()
