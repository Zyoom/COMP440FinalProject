import tkinter as tk
from tkinter import messagebox
from db.database import create_connection
from models.customer import Customer
from models.agent import Agent
from models.email import Email
from services.email_handler import EmailHandler

def add_customer():
    email = customer_email_entry.get()
    if email:
        customer = Customer(connection, email)
        customer.save()
        messagebox.showinfo("Success", "Customer added successfully")
    else:
        messagebox.showerror("Error", "Please enter an email address")

def add_agent():
    name = agent_name_entry.get()
    if name:
        agent = Agent(connection, name)
        agent.save()
        messagebox.showinfo("Success", "Agent added successfully")
    else:
        messagebox.showerror("Error", "Please enter a name")

def send_email():
    subject = email_subject_entry.get()
    body = email_body_entry.get()
    customer_id = int(customer_id_entry.get())
    email_handler.assign_email_to_agent(subject, body, customer_id)
    messagebox.showinfo("Success", "Email sent successfully")

def view_history():
    customer_id = int(customer_id_entry.get())
    emails = email_handler.view_customer_email_history(customer_id)
    email_list.delete(0, tk.END)
    for email in emails:
        email_list.insert(tk.END, f"{email['subject']} - {email['sent_at']}")

# Create main window
root = tk.Tk()
root.title("Email Service Management")

# Create and place widgets
tk.Label(root, text="Customer Email:").grid(row=0, column=0)
customer_email_entry = tk.Entry(root)
customer_email_entry.grid(row=0, column=1)
tk.Button(root, text="Add Customer", command=add_customer).grid(row=0, column=2)

tk.Label(root, text="Agent Name:").grid(row=1, column=0)
agent_name_entry = tk.Entry(root)
agent_name_entry.grid(row=1, column=1)
tk.Button(root, text="Add Agent", command=add_agent).grid(row=1, column=2)

tk.Label(root, text="Subject:").grid(row=2, column=0)
email_subject_entry = tk.Entry(root)
email_subject_entry.grid(row=2, column=1)

tk.Label(root, text="Body:").grid(row=3, column=0)
email_body_entry = tk.Entry(root)
email_body_entry.grid(row=3, column=1)

tk.Label(root, text="Customer ID for Email:").grid(row=4, column=0)
customer_id_entry = tk.Entry(root)
customer_id_entry.grid(row=4, column=1)

tk.Button(root, text="Send Email", command=send_email).grid(row=5, column=1)

tk.Button(root, text="View History", command=view_history).grid(row=6, column=1)

email_list = tk.Listbox(root, height=10, width=50)
email_list.grid(row=7, column=0, columnspan=2)

# Establish connection and handler
print("Creating connection...")
connection = create_connection()
print("Connection created.")

email_handler = EmailHandler(connection)

# Start the GUI event loop
root.mainloop()
