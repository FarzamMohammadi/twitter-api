import datetime
import logging
from flask import Flask, request, session
import sqlite3

conn = sqlite3.connect('database.db', check_same_thread=False)


# DB users table creation
def create_messages_table():
    # Drops table if it already exists
    conn.execute("DROP TABLE IF EXISTS messages")
    conn.execute("CREATE TABLE IF NOT EXISTS messages (sender, receiver, message, read, date)")
    conn.commit()
    

def send_message(receiver, message):
    create_messages_table()
    try:
        sender = session.get('username')
        params = (sender, receiver, message, 0, datetime.datetime.now())
        # If user doesn't exist insert record
        if sender:
            conn.execute("""INSERT INTO messages (sender, receiver, message, read, date)
                                     VALUES(?,?,?,?,?)""", params)
            conn.commit()
            return True
        else:
            return False
    except Exception as e:
        logging.exception(e)
        return False
