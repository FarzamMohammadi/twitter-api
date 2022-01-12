import sqlite3
import bcrypt
from flask import session


conn = sqlite3.connect('database.db', check_same_thread=False)


def check_credentials(username, password):
    user_record = conn.execute("SELECT * FROM users WHERE username = ?", (username,))
    user_exists = user_record.fetchone()
    hash_password = user_exists[1]
    if user_exists:
        # If credentials match DB records sets session variables
        if bcrypt.checkpw(password.encode('utf8'), hash_password.encode('utf8')):
            session['username'] = username
            session['password'] = hash_password
            return True
        else:
            return False
    else:
        return False
