from db.database import create_connection
from models.customer import Customer
from models.agent import Agent
from models.email import Email

def main():
    conn = create_connection()
    if conn is not None:
        # Example usage
        customer = Customer(conn, 'dave16@gmail.com')
        customer.save()

        agent = Agent(conn, 'Dave', '1627')
        agent.save()

        email = Email(conn, 'Hello', 'This is a test email', 1, 1)
        email.send()

        print(customer.get_emails())

if __name__ == "__main__":
    main()
