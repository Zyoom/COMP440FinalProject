import mysql.connector
from mysql.connector import Error

def create_connection():
    """Create a database connection."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="COMP440Project",
            database="Project1",
            port=3306
        )
        print("Connection to MySQL DB successful")
        return connection
    except Error as e:
        print(f"The error '{e}' occurred")
        return None

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
# db/database.py

def execute_read_query(connection, query, params=None):
    cursor = connection.cursor()
    try:
        if params:
            cursor.execute(query, params)  # Use params when provided
        else:
            cursor.execute(query)
        return cursor.fetchall()
    finally:
        cursor.close()

