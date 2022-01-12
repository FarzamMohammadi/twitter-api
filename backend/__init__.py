from .password_handling import password_check, hash_password
from flask import Flask
from flask_restful import Resource, Api
import os
import sqlite3
import logging


conn = sqlite3.connect('database.db', check_same_thread=False)
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12)
api = Api(app)


# DB users table creation
def create_users_table():
    conn.execute("CREATE TABLE IF NOT EXISTS users (username, password)")
    conn.commit()


# Used to insert new user
def insert_new_user(username, password):
    params = (username, hash_password(password).decode())

    try:
        user_record = conn.execute("SELECT rowid FROM users WHERE username = ?", (username,))
        user_exists = user_record.fetchall()
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


class Registration(Resource):
    create_users_table()

    def post(self, username, passowrd):
        if password_check(passowrd):
            if insert_new_user(username, passowrd):
                return {'username': username}, 200
            else:
                return {'error': 'User Exists'}, 500
        else:
            return {'error': 'Invalid Password'}, 500


api.add_resource(Registration, '/register/<string:username>/<string:passowrd>')

