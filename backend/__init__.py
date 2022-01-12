from .register import create_users_table, insert_new_user, password_check, hash_password
from flask import Flask
from flask_restful import Resource, Api
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12)
api = Api(app)


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


class Login(Resource):
    def get(self, username, passowrd):
        return {"MSG": "Welcome"}


api.add_resource(Registration, '/register/<string:username>/<string:passowrd>')
api.add_resource(Login, '/login/<string:username>/<string:passowrd>')

