from db.database import execute_query
class Email:
    def __init__(self, connection, subject, body, customer_id, agent_id, in_reply_to=None):
        self.connection = connection
        self.subject = subject
        self.body = body
        self.customer_id = customer_id
        self.agent_id = agent_id
        self.in_reply_to = in_reply_to

    def send(self):
        in_reply_to_value = 'NULL' if self.in_reply_to is None else self.in_reply_to
        query = f"""
        INSERT INTO Emails (subject, body, customer_id, agent_id, in_reply_to)
        VALUES ('{self.subject}', '{self.body}', {self.customer_id}, {self.agent_id}, {in_reply_to_value})
        """
        execute_query(self.connection, query)

