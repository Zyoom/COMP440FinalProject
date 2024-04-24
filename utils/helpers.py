# utils/helpers.py
import re
import bcrypt
from datetime import datetime

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()

def check_password(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password)

def validate_email(email):
    """Simple regex check for a valid email format."""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

def format_datetime(timestamp):
    """Format datetime object to a readable string."""
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')

def parse_datetime(date_str):
    """Parse a string into a datetime object."""
    return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

