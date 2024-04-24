from db.database import execute_query

class Agent:
    def __init__(self, connection, name):
        self.connection = connection
        self.name = name

    def save(self):
        query = f"INSERT INTO Agents (name) VALUES ('{self.name}')"
        execute_query(self.connection, query)
