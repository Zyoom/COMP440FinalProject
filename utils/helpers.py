# utils/helpers.py
import re
from datetime import datetime

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

