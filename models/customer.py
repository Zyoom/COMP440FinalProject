from db.database import execute_query, execute_read_query

class Customer:
    def __init__(self, connection, email):
        self.connection = connection
        self.email = email

    def save(self):
        query = f"INSERT INTO Customers (email) VALUES ('{self.email}')"
        execute_query(self.connection, query)

    def get_emails(self):
        query = f"SELECT * FROM Emails WHERE customer_id = (SELECT customer_id FROM Customers WHERE email = '{self.email}')"
        return execute_read_query(self.connection, query)
