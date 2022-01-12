import bcrypt
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
    conn.execute("""CREATE TABLE IF NOT EXISTS users
                     (username, password)""")
    conn.commit()


# Used to insert new user
def insert_new_user(username, password):
    # Password encryption
    hashed_pass = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(12))
    params = (username, hashed_pass.decode())

    try:
        conn.execute("""INSERT INTO users (username, password)
                                 VALUES(?,?)""", params)
        conn.commit()
    except Exception as e:
        logging.exception(e)
        pass


# Password validation
def password_check(passowrd):

    SpecialSym = ['$', '@', '#', '%', '/']
    val = True

    if len(passowrd) < 6:
        print('length should be at least 6')
        val = False

    if len(passowrd) > 20:
        print('length should be not be greater than 8')
        val = False

    if not any(char.isdigit() for char in passowrd):
        print('Password should have at least one numeral')
        val = False

    if not any(char.isupper() for char in passowrd):
        print('Password should have at least one uppercase letter')
        val = False

    if not any(char.islower() for char in passowrd):
        print('Password should have at least one lowercase letter')
        val = False

    if not any(char in SpecialSym for char in passowrd):
        print('Password should have at least one of the symbols $@#')
        val = False
    if val:
        return val


class Registration(Resource):
    create_users_table()

    def post(self, username, passowrd):
        if password_check(passowrd):
            insert_new_user(username, passowrd)
            return {'username': username}, 200
        else:
            return {'error': 'Invalid Password'}, 500


api.add_resource(Registration, '/register/<string:username>/<string:passowrd>')

