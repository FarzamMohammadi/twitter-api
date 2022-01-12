from .login import check_credentials
from .register import create_users_table, insert_new_user, password_check, hash_password
from flask import Flask
from flask_session import Session
from flask_restful import Resource, Api
import os


app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(12)
api = Api(app)
Session(app)


class Registration(Resource):
    create_users_table()

    def post(self, username, password):
        if password_check(password):
            if insert_new_user(username, password):
                return {'username': username}, 201
            else:
                return {'error': 'User Exists'}, 409
        else:
            return {'error': 'Invalid Password'}, 500


class Login(Resource):
    def post(self, username, password):
        if check_credentials(username, password):
            return {"Message": "Login Successful"}, 200
        else:
            return {'error': 'Invalid Password'}, 401


api.add_resource(Registration, '/register/<string:username>/<string:password>')
api.add_resource(Login, '/login/<string:username>/<string:password>')

