import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="*yv7YZybeXC#f#",
    database="comp440project",
    port=3306
)
cursor = conn.cursor()

# Define your models: Customer, Email, Agent

class Customer:
    def __init__(self, email):
        self.email = email
        self.id = None  # Will be set after insertion into database

    def save(self):
        cursor.execute("INSERT INTO Customers (email) VALUES (%s)", (self.email,))
        conn.commit()
        self.id = cursor.lastrowid

class Email:
    def __init__(self, subject, body, customer_id, agent_id):
        self.subject = subject
        self.body = body
        self.customer_id = customer_id
        self.agent_id = agent_id
        self.in_reply_to_id = None  # Will be set if it's a reply
        self.id = None  # Will be set after insertion into database

    def save(self):
        cursor.execute("INSERT INTO Emails (subject, body, customer_id, agent_id, in_reply_to) "
                       "VALUES (%s, %s, %s, %s, %s)",
                       (self.subject, self.body, self.customer_id, self.agent_id, self.in_reply_to_id))
        conn.commit()
        self.id = cursor.lastrowid

class Agent:
    def __init__(self, name):
        self.name = name
        self.id = None  # Will be set after insertion into database

    def save(self):
        cursor.execute("INSERT INTO Agents (name) VALUES (%s)", (self.name,))
        conn.commit()
        self.id = cursor.lastrowid
