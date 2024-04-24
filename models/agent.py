# models/agent.py
from db.database import execute_query, execute_read_query



# agent.py within the 'models' directory

# agent.py within the 'models' directory

class Agent:
    def __init__(self, connection, name, password):
        self.connection = connection
        self.name = name
        self.password = password

    def save(self):
        # Assuming you're directly storing the passwords (not recommended)
        query = "INSERT INTO Agents (name, password) VALUES (%s, %s)"
        cursor = self.connection.cursor()
        cursor.execute(query, (self.name, self.password))
        self.connection.commit()
        cursor.close()

    @staticmethod
    def authenticate(connection, name, password):
        query = "SELECT password FROM Agents WHERE name = %s"
        cursor = connection.cursor()
        cursor.execute(query, (name,))
        result = cursor.fetchone()
        cursor.close()
        if result and result[0] == password:
            return True
        return False

