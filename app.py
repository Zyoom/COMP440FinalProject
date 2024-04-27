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

    agent_id = agent_id + 1
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
            #print("Agent ID stored in session:", session['agent_id'])
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
    # Render the agent dashboard template with emails
    return render_template('agent_dashboard.html', emails=emails)



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

    # Assuming the column names are: email_id, subject, body, customer_id, agent_id
    # You can adjust these column names according to your database schema
    email_data = {
        'email_id': email[0],
        'subject': email[1],
        'body': email[2],
        'customer_email': customer_email,
        'agent_id': email[4],
        'replies': replies
    }

    return render_template('view_email.html', email=email_data)


@app.route('/agent/email/<int:email_id>/reply', methods=['GET', 'POST'])
def reply_to_email(email_id):
    if request.method == 'POST':
        # Handle agent's reply to the email
        reply_text = request.form['reply_text']
        agent_id = session['agent_id']  # Assuming agent is logged in
        # Save the reply to the database and associate it with the email
        cursor.execute("INSERT INTO Replies (email_id, agent_id, reply_text) VALUES (%s, %s, %s)",
                       (email_id, agent_id, reply_text))
        models.conn.commit()
        return redirect(url_for('view_email', email_id=email_id))
    else:
        # Render the reply form for the agent
        return render_template('reply_email.html', email_id=email_id)

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

if __name__ == '__main__':
    app.run(debug=True)
    serve(app, host="0.0.0.0", port=8080)
