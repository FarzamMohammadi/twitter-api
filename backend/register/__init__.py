from .password_handler import password_check, hash_password
import sqlite3
import logging

conn = sqlite3.connect('database.db', check_same_thread=False)


# DB users table creation
def create_users_table():
    # Drops table if it already exists
    # conn.execute("DROP TABLE IF EXISTS users")
    conn.execute("CREATE TABLE IF NOT EXISTS users (username, password)")
    conn.commit()


# Used to insert new user
def insert_new_user(username, password):
    create_users_table()
    params = (username, hash_password(password).decode())

    try:
        user_record = conn.execute("SELECT * FROM users WHERE username = ?", (username,))
        user_exists = user_record.fetchone()
        # If user doesn't exist insert record
        if not user_exists:
            conn.execute("""INSERT INTO users (username, password)
                                     VALUES(?,?)""", params)
            conn.commit()
            return True
        else:
            return False

    except Exception as e:
        logging.exception(e)
        return False


