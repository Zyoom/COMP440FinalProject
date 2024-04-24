from models.email import Email
from models.agent import Agent

class EmailHandler:
    def __init__(self, connection):
        self.connection = connection

    def assign_email_to_agent(self, subject, body, customer_id, in_reply_to=None):
        """
        Assigns an incoming email to an agent. If the email is a reply, tries to assign it to the same agent who handled the previous email.
        """
        # Try to find the previous agent if this is a reply
        if in_reply_to:
            previous_email = self.get_email_by_id(in_reply_to)
            agent_id = previous_email['agent_id'] if previous_email else self.find_available_agent()
        else:
            agent_id = self.find_available_agent()

        # Create and send email
        email = Email(self.connection, subject, body, customer_id, agent_id, in_reply_to)
        email.send()
        print(f"Email assigned to agent {agent_id} and sent.")

    def get_email_by_id(self, email_id):
        """
        Retrieves an email by its ID.
        """
        query = f"SELECT * FROM Emails WHERE email_id = {email_id}"
        emails = execute_read_query(self.connection, query)
        return emails[0] if emails else None

    def find_available_agent(self):
        """
        Find the first available agent. This is a placeholder function; implement your own logic for agent availability.
        """
        query = "SELECT agent_id FROM Agents LIMIT 1"
        agents = execute_read_query(self.connection, query)
        return agents[0]['agent_id'] if agents else None

    def view_customer_email_history(self, customer_id):
        """
        Retrieves the history of all emails associated with a specific customer.
        """
        query = f"SELECT * FROM Emails WHERE customer_id = {customer_id} ORDER BY sent_at DESC"
        return execute_read_query(self.connection, query)
