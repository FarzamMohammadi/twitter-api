from flask import Flask
from flask_restful import Resource, Api
import os
import sqlite3
import logging


conn = sqlite3.connect('database.db', check_same_thread=False)
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12)
api = Api(app)


def create_users_table():
    conn.execute("""CREATE TABLE IF NOT EXISTS users
                     (username, password)""")
    conn.commit()


def insert_new_user(username, password):
    params = (username, password)
    try:
        conn.execute("""INSERT INTO users (username, password)
                                 VALUES(?,?)""", params)
        conn.commit()
    except Exception as e:
        logging.exception(e)
        pass


class Registration(Resource):
    create_users_table()

    def post(self, username, passowrd):
        insert_new_user(username, passowrd)
        return {'username': username}, 200


api.add_resource(Registration, '/register/<string:username>/<string:passowrd>')

