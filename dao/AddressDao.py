from database.DatabaseConnector import disconnect_from_mysql, connect_to_mysql
from models.Address import Address
from models.MyResponse import MyResponse


def create_address(address: Address) -> MyResponse:
    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        query = ("INSERT INTO VisitorTracking.Address "
                 "(street, number, postcode, city, floor) "
                 "VALUES (%s, %s, %s, %s, %s)")
        cursor.execute(query,
                       (address.street, address.number, address.postcode, address.city, address.floor))
        connection.commit()

        return MyResponse("Address created successfully", response_code=MyResponse.CREATED)
    except Exception as err:
        return MyResponse(f"Error creating address: {err}", response_code=MyResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def fetch_addresses() -> MyResponse:
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
            return MyResponse("No addresses found", response_code=MyResponse.NOT_FOUND)

        return MyResponse(addresses, response_code=MyResponse.OK)
    except Exception as err:
        print(f"Error retrieving addresses: {err}")
        return MyResponse("Error retrieving addresses", response_code=MyResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def get_address_by_id(address_id: int) -> MyResponse:
    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        query = "SELECT * FROM VisitorTracking.Address WHERE id = %s"
        cursor.execute(query, (address_id,))
        row = cursor.fetchone()

        if row:
            address = Address(address_id=row[0], street=row[1], number=row[2], postcode=row[3], city=row[4],
                              floor=row[5])
            return MyResponse(response=address, response_code=MyResponse.OK)
        else:
            return MyResponse(response="Address not found", response_code=MyResponse.NOT_FOUND)
    except Exception as error:
        return MyResponse(response=f"Error retrieving address by ID: {error}", response_code=MyResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def update_address(address: Address) -> MyResponse:
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
            return MyResponse("Address updated successfully", MyResponse.OK)
        else:
            return MyResponse("Address not found", MyResponse.NOT_FOUND)
    except Exception as error:
        print("Error updating address:", error)
        return MyResponse("Error updating address", MyResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def delete_address(address_id: int) -> MyResponse:
    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        query = "DELETE FROM VisitorTracking.Address WHERE id = %s"
        cursor.execute(query, (address_id,))
        connection.commit()

        if cursor.rowcount > 0:
            return MyResponse("Address deleted successfully", MyResponse.OK)
        else:
            return MyResponse("Address not found", MyResponse.NOT_FOUND)
    except Exception as error:
        print("Error deleting address:", error)
        return MyResponse("Error deleting address", MyResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def check_address_exists(address: Address) -> int:
    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        query = """
            SELECT id
            FROM VisitorTracking.Address
            WHERE
                street = %s
                AND number = %s
                AND postcode = %s
                AND city = %s
                AND (floor = %s OR floor IS NULL);
        """

        cursor.execute(query, (address.street, address.number, address.postcode, address.city, address.floor))
        result = cursor.fetchone()
        if result:
            print("ID found:", result[0])
            return result[0]
        else:
            print("Address not found")
            return -1
    except Exception as error:
        print("Error checking address existence:", error)
        return -1
    finally:
        cursor.close()
        disconnect_from_mysql(connection)
