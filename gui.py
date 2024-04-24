import tkinter as tk
from tkinter import messagebox, simpledialog
from db.database import create_connection
from models.customer import Customer
from models.agent import Agent
from models.email import Email
from services.email_handler import EmailHandler


# Authentication window
def show_login_window():
    login_window = tk.Toplevel()
    login_window.title("Agent Login")

    tk.Label(login_window, text="Agent Name:").grid(row=0, column=0)
    agent_name_entry = tk.Entry(login_window)
    agent_name_entry.grid(row=0, column=1)

    tk.Label(login_window, text="Password:").grid(row=1, column=0)
    agent_password_entry = tk.Entry(login_window, show="*")
    agent_password_entry.grid(row=1, column=1)

    tk.Button(login_window, text="Login",
              command=lambda: login(agent_name_entry.get(), agent_password_entry.get(), login_window)).grid(row=2,
                                                                                                            column=1)


def login(agent_name, password, window):
    if agent_name and password:  # Simple authentication check
        global current_agent_id
        if Agent.authenticate(connection, agent_name, password):
            current_agent_id = agent_name  # Store agent's name or an identifier
            window.destroy()
            messagebox.showinfo("Login Success", "You are logged in.")
        else:
            messagebox.showerror("Login Failed", "The username or password is incorrect")
    else:
        messagebox.showerror("Login Failed", "Please enter both username and password")


def add_customer():
    email = customer_email_entry.get()
    if email:
        customer = Customer(connection, email)
        customer.save()
        messagebox.showinfo("Success", "Customer added successfully")
    else:
        messagebox.showerror("Error", "Please enter a customer email")


def add_agent():
    agent_window = tk.Toplevel()
    agent_window.title("Add Agent")

    tk.Label(agent_window, text="Agent Name:").grid(row=0, column=0)
    name_entry = tk.Entry(agent_window)
    name_entry.grid(row=0, column=1)

    tk.Label(agent_window, text="Password:").grid(row=1, column=0)
    password_entry = tk.Entry(agent_window, show="*")
    password_entry.grid(row=1, column=1)

    def submit_agent():
        name = name_entry.get()
        password = password_entry.get()
        if name and password:
            agent = Agent(connection, name, password)
            agent.save()
            messagebox.showinfo("Success", "Agent added successfully")
            agent_window.destroy()
        else:
            messagebox.showerror("Error", "Both name and password are required")

    tk.Button(agent_window, text="Submit", command=submit_agent).grid(row=2, column=1)

    # Remove any duplicate button bindings for adding an agent
    tk.Button(root, text="Add Agent", command=add_agent).grid(row=1, column=2)




def send_email():
    subject = email_subject_entry.get()
    body = email_body_entry.get()
    customer_id = simpledialog.askinteger("Input", "Enter customer ID")
    if subject and body and customer_id:
        email = Email(connection, subject, body, customer_id, current_agent_id)
        email.send()
        messagebox.showinfo("Success", "Email sent successfully")
    else:
        messagebox.showerror("Error", "Please fill out all fields")


def send_reply():
    if email_list.curselection():
        selected_index = email_list.curselection()[0]
        selected_email = email_list.get(selected_index)
        email_id = int(selected_email.split('-')[0].strip())
        customer_id = simpledialog.askinteger("Input", "Enter customer ID for the reply")

        subject = "Re: " + email_subject_entry.get()
        body = email_body_entry.get()

        if subject and body:
            email_handler.assign_email_to_agent(subject, body, customer_id, in_reply_to=email_id)
            messagebox.showinfo("Success", "Reply sent successfully")
        else:
            messagebox.showerror("Error", "Please fill out all fields")
    else:
        messagebox.showerror("Error", "No email selected for reply")


def view_history():
    customer_id = simpledialog.askinteger("Input", "Enter customer ID to view history")
    if customer_id:
        emails = email_handler.view_customer_email_history(customer_id)
        email_list.delete(0, tk.END)
        for email in emails:
            email_list.insert(tk.END, f"{email['email_id']} - {email['subject']} - {email['sent_at']}")


# Initialize GUI
root = tk.Tk()
root.title("Email Service Management")

current_agent_id = None  # Global to store the current agent's ID
show_login_window()  # Show login on start

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

tk.Button(root, text="Send Email", command=send_email).grid(row=4, column=1)
tk.Button(root, text="Reply to Email", command=send_reply).grid(row=5, column=1)
tk.Button(root, text="View History", command=view_history).grid(row=6, column=1)

email_list = tk.Listbox(root, height=10, width=50)
email_list.grid(row=7, column=0, columnspan=3)

# Establish connection and handler
print("Creating connection...")
connection = create_connection()
print("Connection created.")

email_handler = EmailHandler(connection)

# Start the GUI event loop
root.mainloop()
