from flask import Flask, render_template, request, redirect, url_for, session
import models
import templates
from models import cursor
from waitress import serve
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
users = {
    'Agent1': {'password': 'password1', 'agent_id': 1},
    'Agent2': {'password': 'password2', 'agent_id': 2}
}


@app.route('/')
def index():
    # Fetch agents
    cursor.execute("SELECT * FROM Agents")
    agents = cursor.fetchall()
    return render_template('index.html', agents=agents)


@app.route('/emails/<int:agent_id>')
def show_emails(agent_id):
    # Fetch emails for the specified agent
    agent_id = agent_id + 1
    cursor.execute("SELECT * FROM Emails WHERE agent_id = %s", (agent_id,))
    emails = cursor.fetchall()
    return render_template('emails.html', emails=emails, agent_id=agent_id)


@app.route('/assign', methods=['POST'])
def assign_email():
    subject = request.form['subject']
    body = request.form['body']
    customer_email = request.form['customer_email']

    # Check if the customer already exists
    cursor.execute("SELECT id FROM Customers WHERE email = %s", (customer_email,))
    customer = cursor.fetchone()
    if not customer:
        new_customer = models.Customer(email=customer_email)
        new_customer.save()
        customer_id = new_customer.id
    else:
        customer_id = customer[0]

    # Retrieve agent_id from the session
    agent_id = session.get('agent_id')
    if agent_id is None:
        # If agent_id is not in session, redirect to login page
        return redirect(url_for('login'))

    # Save the email
    new_email = models.Email(subject=subject, body=body, customer_id=customer_id, agent_id=agent_id)
    new_email.save()

    return redirect(url_for('show_emails', agent_id=agent_id))

#for agents
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            # Authentication successful, set session data
            session['username'] = username
            session['agent_id'] = users[username]['agent_id']
            return redirect(url_for('agent_dashboard'))
        else:
            # Authentication failed, redirect to login page with an error message
            return render_template('login.html', error='Invalid username or password')

    # If method is GET, render the login form
    return render_template('login.html')





@app.route('/logout')
def logout():
    # Clear session data (logout)
    session.pop('username', None)
    session.pop('agent_id', None)
    return redirect(url_for('index'))


@app.route('/agent/dashboard')
def agent_dashboard():
    if 'username' not in session:
        # If user is not logged in, redirect to login page
        return redirect(url_for('login'))

    # Retrieve agent_id from session
    agent_id = session.get('agent_id')
    if agent_id is None:
        # If agent_id is not in session, redirect to login page
        return redirect(url_for('login'))

    # Fetch the agent's name from the database based on the agent_id
    cursor.execute("SELECT name FROM Agents WHERE id = %s", (agent_id,))
    agent_data = cursor.fetchone()
    agent_name = agent_data[0] if agent_data else None

    # Fetch emails for the logged-in agent
    cursor.execute("SELECT * FROM Emails")
    emails_data = cursor.fetchall()
    emails = []
    for email_tuple in emails_data:
        email_dict = {
            'email_id': email_tuple[0],
            'subject': email_tuple[1],
            'body': email_tuple[2],
            # Add other fields here
        }
        emails.append(email_dict)

    # Render the agent dashboard template with emails and agent's name
    return render_template('agent_dashboard.html', emails=emails, agent_name=agent_name)




@app.route('/agent/email/<int:email_id>/delete', methods=['POST'])
def delete_email(email_id):
    # Perform deletion of the email with the specified email_id
    # For example:
    cursor.execute("DELETE FROM Emails WHERE id = %s", (email_id,))
    models.conn.commit()
    # Redirect back to the agent dashboard after deletion
    return redirect(url_for('agent_dashboard'))


@app.route('/agent/email/<int:email_id>')
def view_email(email_id):
    # Fetch the details of the specified email from the database
    cursor.execute("SELECT * FROM Emails WHERE id = %s", (email_id,))
    email = cursor.fetchone()

    # Fetch the customer's email address associated with the email
    cursor.execute("SELECT email FROM Customers WHERE id = %s", (email[3],))
    customer_email = cursor.fetchone()[0]  # Assuming email is the first column

    # Fetch the conversation history (replies) associated with the email
    cursor.execute("SELECT agent_id, reply_text, reply_date FROM Replies WHERE email_id = %s", (email_id,))
    replies = cursor.fetchall()

    # Fetch the customer's replies associated with the email
    cursor.execute("SELECT customer_email, reply_text, reply_date FROM UserReplies WHERE email_id = %s", (email_id,))
    customer_replies = cursor.fetchall()

    # Assuming the column names are: email_id, subject, body, customer_id, agent_id
    # You can adjust these column names according to your database schema
    email_data = {
        'email_id': email[0],
        'subject': email[1],
        'body': email[2],
        'customer_email': customer_email,
        'agent_id': email[4],
        'replies': replies,
        'customer_replies': customer_replies
    }

    return render_template('view_email.html', email=email_data)


@app.route('/agent/email/<int:email_id>/reply', methods=['GET', 'POST'])
def reply_to_email(email_id):
    if request.method == 'POST':
        if 'username' not in session:
            return redirect(url_for('login'))  # Redirect if user is not logged in

        # Handle agent's reply to the email
        reply_text = request.form['reply_text']
        agent_id = session.get('agent_id')  # Retrieve agent_id from session

        # Save the reply to the database and associate it with the email
        cursor.execute("INSERT INTO Replies (email_id, agent_id, reply_text) VALUES (%s, %s, %s)",
                       (email_id, agent_id, reply_text))
        models.conn.commit()
        return redirect(url_for('view_email', email_id=email_id))
    else:
        # Render the reply form for the agent
        return render_template('reply_email.html', email_id=email_id)

@app.route('/view_sent_emails')
def view_sent_emails():
    # Retrieve all emails and their replies (both agent and customer) from the database
    cursor.execute("SELECT * FROM Emails")
    user_emails_data = cursor.fetchall()

    user_emails = []
    for email_tuple in user_emails_data:
        email_dict = {
            'email_id': email_tuple[0],
            'subject': email_tuple[1],
            'body': email_tuple[2],
            'replies': []  # Placeholder for both agent and customer replies
        }
        # Fetch agent replies for each email
        cursor.execute("SELECT reply_text FROM Replies WHERE email_id = %s", (email_tuple[0],))
        replies_data = cursor.fetchall()
        for reply in replies_data:
            email_dict['replies'].append(('Agent', reply[0]))  # Append agent replies

        # Fetch customer replies for each email
        cursor.execute("SELECT reply_text FROM UserReplies WHERE email_id = %s", (email_tuple[0],))
        customer_replies_data = cursor.fetchall()
        for reply in customer_replies_data:
            email_dict['replies'].append(('Customer', reply[0]))  # Append customer replies

        user_emails.append(email_dict)

    return render_template('view_sent_email.html', emails=user_emails)

@app.route('/user/email/<int:email_id>/reply', methods=['POST'])
def reply_to_agent_email(email_id):
    if request.method == 'POST':
        username = session.get('username')
        if not username:
            # If user is not logged in, handle appropriately (e.g., redirect to login page)
            return redirect(url_for('login'))

        # Handle user's reply to the agent's email
        reply_text = request.form['reply_text']

        # Fetch the customer_id from the Emails table based on the email_id
        cursor.execute("SELECT customer_id FROM Emails WHERE id = %s", (email_id,))
        customer_id = cursor.fetchone()[0]

        # Save the reply to the database and associate it with the email and customer_id
        cursor.execute("INSERT INTO UserReplies (email_id, customer_id, reply_text, reply_date) VALUES (%s, %s, %s, CURRENT_TIMESTAMP)",
                       (email_id, customer_id, reply_text))
        models.conn.commit()
        return redirect(url_for('view_sent_emails'))

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

if __name__ == '__main__':
    app.run(debug=True)
    serve(app, host="0.0.0.0", port=8080)