import json
from werkzeug.security import check_password_hash

# db_users = {
#     'chuck': {'password': 'norris', 'roles': ['admin']},
#     'lee': {'password': 'douglas', 'roles': []},
#     'mary': {'password': 'jane', 'roles': []},
#     'steven': {'password': 'wilson', 'roles': ['admin']}
# }

def check_users(user):
    """Check if user exists and its credentials.
    Take a look at encrypt_app.py and encrypt_cli.py
     to see how to encrypt passwords
    """
    db_users = json.load(open('users.json'))
    user_data = db_users.get(user['username'])
    if not user_data:
        return False  # <--- invalid credentials
    elif check_password_hash(user_data.get('password'), user['password']):
        return True  # <--- user is logged in!
    return False  # <--- invalid credentials
#
# def check_users(user):
#     """Check if user exists and its credentials.
#     Take a look at encrypt_app.py and encrypt_cli.py
#      to see how to encrypt passwords
#     """
#     db_users = json.load(open('users.json'))
#     user_data = db_users.get(user['username'])
#     # import pdb; pdb.set_trace()
#     if not user_data:
#         return False  # <--- invalid credentials
#     elif user_data.get('password') == user['password']:
#         return True  # <--- user is logged in!


def be_admin(username):
    """Validator to check if user has admin role"""
    db_users = json.load(open('users.json'))
    user_data = db_users.get(username)
    if not user_data or 'admin' not in user_data.get('roles', []):
        return "User does not have admin role"


def have_approval(username):
    """Validator: all users approved, return None"""
    return



