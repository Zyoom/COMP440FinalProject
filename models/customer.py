from db.database import execute_query, execute_read_query

# models/customer.py

class Customer:
    def __init__(self, connection, email):
        self.connection = connection
        self.email = email

    def email_exists(self):
        query = f"SELECT EXISTS(SELECT 1 FROM Customers WHERE email='{self.email}')"
        cursor = self.connection.cursor()
        cursor.execute(query)
        exists = cursor.fetchone()[0]
        return exists

    def save(self):
        if not self.email_exists():
            query = f"INSERT INTO Customers (email) VALUES ('{self.email}')"
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            print("Customer added successfully")
        else:
            print("Email already exists.")
