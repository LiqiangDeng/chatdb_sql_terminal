import mysql.connector

def connect_to_database():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="my_dsci"
    )
    return connection

# A special method for running SQL queries, used for special processing of table related logic
def execute_sql_tables_query(sql_query):
    connection = connect_to_database()
    cursor = connection.cursor()

    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        return results
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

# Mainly used for running regular SQL statements, returning results item by item
def execute_sql_query(sql_query):
    connection = connect_to_database()
    cursor = connection.cursor()

    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        for row in results:
            print(row)
        return results
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()