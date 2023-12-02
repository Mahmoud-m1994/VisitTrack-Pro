from database.DatabaseConnector import connect_to_mysql, disconnect_from_mysql
from models.Company import Company
from models.Address import Address
from dao.AddressDao import check_address_exists
from models.MyResponse import MyResponse


def create_company(company: Company, address: Address) -> MyResponse:
    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        connection.start_transaction()
        address_id = check_address_exists(address)

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
                return MyResponse("Error creating address for given Company", MyResponse.ERROR)

        query = ("INSERT INTO VisitorTracking.company "
                 "(id, name, address_id) "
                 "VALUES (%s, %s, %s)")

        cursor.execute(query, (company.company_id, company.name, address_id))
        connection.commit()
        if cursor.rowcount > 0:
            return MyResponse("Company created successfully", response_code=MyResponse.CREATED)
        else:
            return MyResponse("Company insertion failed,", response_code=MyResponse.ERROR)
    except Exception as err:
        connection.rollback()
        return MyResponse(f"Error creating Company: {err}", response_code=MyResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def fetch_all_companies() -> MyResponse:
    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        query = "SELECT * FROM VisitorTracking.company ORDER BY id DESC"
        cursor.execute(query)
        rows = cursor.fetchall()

        companies = []
        for row in rows:
            company = Company(
                company_id=row[0], name=row[1], address_id=row[2]
            )
            companies.append(company)

        if len(companies) == 0:
            return MyResponse("No companies found", response_code=MyResponse.NOT_FOUND)

        return MyResponse(companies, response_code=MyResponse.OK)
    except Exception as err:
        print(f"Error retrieving companies: {err}")
        return MyResponse("Error retrieving companies", response_code=MyResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def get_company_by_id(company_id: int) -> MyResponse:
    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        query = "SELECT * FROM VisitorTracking.company WHERE id = %s"
        cursor.execute(query, (company_id,))
        row = cursor.fetchone()

        if row:
            company = Company(
                company_id=row[0], name=row[1], address_id=row[2]
            )
            return MyResponse(response=company, response_code=MyResponse.OK)
        else:
            return MyResponse(response="Company not found", response_code=MyResponse.NOT_FOUND)
    except Exception as error:
        return MyResponse(response=f"Error retrieving company by ID: {error}", response_code=MyResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def update_company(company: Company, address: Address = None) -> MyResponse:
    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        connection.start_transaction()

        if address is not None:
            address_id = check_address_exists(address)

            if address_id < 0:  # address not found, create a new one
                insert_address_query = (
                    "INSERT INTO VisitorTracking.Address "
                    "(street, number, postcode, city, floor) "
                    "VALUES (%s, %s, %s, %s, %s)"
                )
                cursor.execute(
                    insert_address_query,
                    (
                        address.street,
                        address.number,
                        address.postcode,
                        address.city,
                        address.floor,
                    ),
                )
                connection.commit()

                address_id = cursor.lastrowid

                if address_id is None or address_id <= 0:
                    connection.rollback()
                    return MyResponse("Error creating address for given company", MyResponse.ERROR)

            # Update the company's address_id with the newly created or existing address_id
            update_company_query = (
                "UPDATE VisitorTracking.company "
                "SET name = %s, address_id = %s WHERE id = %s"
            )
            cursor.execute(update_company_query, (company.name, address_id, company.company_id))
            connection.commit()

        else:
            # Update only the company name
            update_company_query = (
                "UPDATE VisitorTracking.company "
                "SET name = %s WHERE id = %s"
            )
            cursor.execute(update_company_query, (company.name, company.company_id))
            connection.commit()

        if cursor.rowcount > 0:
            return MyResponse("Company updated successfully", MyResponse.OK)
        else:
            return MyResponse("Company not found", MyResponse.NOT_FOUND)

    except Exception as error:
        connection.rollback()
        print("Error updating company:", error)
        return MyResponse("Error updating company", MyResponse.ERROR)

    finally:
        cursor.close()
        disconnect_from_mysql(connection)


def delete_company(company_id: int) -> MyResponse:
    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        query = "DELETE FROM VisitorTracking.company WHERE id = %s"
        cursor.execute(query, (company_id,))
        connection.commit()

        if cursor.rowcount > 0:
            return MyResponse("Company deleted successfully", MyResponse.OK)
        else:
            return MyResponse("Company not found", MyResponse.NOT_FOUND)
    except Exception as error:
        print("Error deleting company:", error)
        return MyResponse("Error deleting company", MyResponse.ERROR)
    finally:
        cursor.close()
        disconnect_from_mysql(connection)
