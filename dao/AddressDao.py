from database.DatabaseConnector import disconnect_from_mysql, connect_to_mysql
from models.Address import Address
from models.MySqlResponse import MySqlResponse


def create_address(address: Address) -> MySqlResponse:
    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        query = ("INSERT INTO VisitorTracking.Address "
                 "(street, number, postcode, city, floor) "
                 "VALUES (%s, %s, %s, %s, %s)")
        cursor.execute(query,
                       (address.street, address.number, address.postcode, address.city, address.floor))
        connection.commit()

        return MySqlResponse("Address created successfully", response_code=MySqlResponse.CREATED)
    except Exception as err:
        return MySqlResponse(f"Error creating address: {err}", response_code=MySqlResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def fetch_addresses() -> MySqlResponse:
    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        query = "SELECT * FROM VisitorTracking.Address ORDER BY id DESC"
        cursor.execute(query)
        rows = cursor.fetchall()

        addresses = []
        for row in rows:
            address = Address(address_id=row[0], street=row[1], number=row[2], postcode=row[3], city=row[4],
                              floor=row[5])
            addresses.append(address)

        if len(addresses) == 0:
            return MySqlResponse("No addresses found", response_code=MySqlResponse.NOT_FOUND)

        return MySqlResponse(addresses, response_code=MySqlResponse.OK)
    except Exception as err:
        print(f"Error retrieving addresses: {err}")
        return MySqlResponse("Error retrieving addresses", response_code=MySqlResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def get_address_by_id(address_id: int) -> MySqlResponse:
    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        query = "SELECT * FROM VisitorTracking.Address WHERE id = %s"
        cursor.execute(query, (address_id,))
        row = cursor.fetchone()

        if row:
            address = Address(address_id=row[0], street=row[1], number=row[2], postcode=row[3], city=row[4],
                              floor=row[5])
            return MySqlResponse(response=address, response_code=MySqlResponse.OK)
        else:
            return MySqlResponse(response="Address not found", response_code=MySqlResponse.NOT_FOUND)
    except Exception as error:
        return MySqlResponse(response=f"Error retrieving address by ID: {error}", response_code=MySqlResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def update_address(address: Address) -> MySqlResponse:
    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        query = ("UPDATE VisitorTracking.Address "
                 "SET street = %s, number = %s, postcode = %s, city = %s, floor = %s "
                 "WHERE id = %s")
        cursor.execute(query,
                       (address.street, address.number, address.postcode, address.city, address.floor,
                        address.address_id))
        connection.commit()

        if cursor.rowcount > 0:
            return MySqlResponse("Address updated successfully", MySqlResponse.OK)
        else:
            return MySqlResponse("Address not found", MySqlResponse.NOT_FOUND)
    except Exception as error:
        print("Error updating address:", error)
        return MySqlResponse("Error updating address", MySqlResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def delete_address(address_id: int) -> MySqlResponse:
    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        query = "DELETE FROM VisitorTracking.Address WHERE id = %s"
        cursor.execute(query, (address_id,))
        connection.commit()

        if cursor.rowcount > 0:
            return MySqlResponse("Address deleted successfully", MySqlResponse.OK)
        else:
            return MySqlResponse("Address not found", MySqlResponse.NOT_FOUND)
    except Exception as error:
        print("Error deleting address:", error)
        return MySqlResponse("Error deleting address", MySqlResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)
