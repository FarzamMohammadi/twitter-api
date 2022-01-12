import datetime
import logging
from flask import Flask, request, session
import sqlite3

conn = sqlite3.connect('database.db', check_same_thread=False)


# DB users table creation
def create_messages_table():
    # Drops table if it already exists
    # conn.execute("DROP TABLE IF EXISTS messages")
    conn.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, sender, receiver, message, read, date)")
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


def set_messages_to_read(messages):
    for msg in messages:
        params = (datetime.datetime.now(), msg[0])
        conn.execute("UPDATE messages SET read=1, date=? WHERE id=?", params)
        conn.commit()


def check_unread_msgs(sender):
    try:
        receiver = session.get('username')
        # If user doesn't exist insert record
        if receiver:
            unread_messages = conn.execute("SELECT * FROM messages WHERE sender = ? AND receiver = ? AND read = 0",
                                           (sender, receiver))
            messages = unread_messages.fetchall()
            set_messages_to_read(messages)
            return messages

    except Exception as e:
        logging.exception(e)
        return False
