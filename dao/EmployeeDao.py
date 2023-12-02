from database.DatabaseConnector import connect_to_mysql, disconnect_from_mysql
from models.Address import Address
from models.MyResponse import MyResponse
from dao.AddressDao import create_address, check_address_exists
from models.Employee import Employee


def create_employee(employee: Employee, address: Address = None) -> MyResponse:
    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        connection.start_transaction()
        address_id = None
        if address is not None:
            address_id = check_address_exists(address=address)
            print("address_id == ", address_id)

            if address_id < 0:  # address not found
                insert_address_query = ("INSERT INTO VisitorTracking.Address "
                                        "(street, number, postcode, city, floor) "
                                        "VALUES (%s, %s, %s, %s, %s)")
                cursor.execute(insert_address_query,
                               (address.street, address.number, address.postcode, address.city, address.floor))
                connection.commit()

                address_id = cursor.lastrowid

                if address_id is None or address_id <= 0:
                    connection.rollback()
                    return MyResponse("Error creating address for given employee", MyResponse.ERROR)

        query = ("INSERT INTO VisitorTracking.employee "
                 "(name, mail, phone, address_id) "
                 "VALUES (%s, %s, %s, %s)")
        cursor.execute(query, (employee.name, employee.mail, employee.phone, address_id))
        connection.commit()

        return MyResponse("Employee created successfully", response_code=MyResponse.CREATED)
    except Exception as err:
        connection.rollback()
        return MyResponse(f"Error creating employee: {err}", response_code=MyResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def fetch_employees() -> MyResponse:
    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        query = "SELECT * FROM VisitorTracking.employee ORDER BY id DESC"
        cursor.execute(query)
        rows = cursor.fetchall()

        employees = []
        for row in rows:
            employee = Employee(employee_id=row[0], name=row[1], mail=row[2], phone=row[3],
                                address_id=row[4])
            employees.append(employee)

        if len(employees) == 0:
            return MyResponse("No employees found", response_code=MyResponse.NOT_FOUND)

        return MyResponse(employees, response_code=MyResponse.OK)
    except Exception as err:
        print(f"Error retrieving employees: {err}")
        return MyResponse("Error retrieving employees", response_code=MyResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def get_employee_by_id(employee_id: int) -> MyResponse:
    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        query = "SELECT * FROM VisitorTracking.employee WHERE id = %s"
        cursor.execute(query, (employee_id,))
        row = cursor.fetchone()

        if row:
            employee = Employee(employee_id=row[0], name=row[1], mail=row[2], phone=row[3], address_id=row[4])
            return MyResponse(response=employee, response_code=MyResponse.OK)
        else:
            return MyResponse(response="employee not found", response_code=MyResponse.NOT_FOUND)
    except Exception as error:
        return MyResponse(response=f"Error retrieving employee by ID: {error}", response_code=MyResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def update_employee(employee: Employee) -> MyResponse:
    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        query = ("UPDATE VisitorTracking.employee "
                 "SET name = %s, mail = %s, phone = %s WHERE id = %s")
        cursor.execute(query, (employee.name, employee.mail, employee.phone, employee.employee_id))
        connection.commit()

        if cursor.rowcount > 0:
            return MyResponse("employee updated successfully", MyResponse.OK)
        else:
            return MyResponse("employee not found", MyResponse.NOT_FOUND)
    except Exception as error:
        print("Error updating employee:", error)
        return MyResponse("Error updating employee", MyResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def delete_employee(employee_id: int) -> MyResponse:
    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        query = "DELETE FROM VisitorTracking.employee WHERE id = %s"
        cursor.execute(query, (employee_id,))
        connection.commit()

        if cursor.rowcount > 0:
            return MyResponse("employee deleted successfully", MyResponse.OK)
        else:
            return MyResponse("employee not found", MyResponse.NOT_FOUND)
    except Exception as error:
        print("Error deleting employee:", error)
        return MyResponse("Error deleting employee", MyResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)
