from .login import check_credentials
from .register import insert_new_user, password_check, hash_password
from .chat import send_message
from flask import Flask, request, session
from flask_session import Session
from flask_restful import Resource, Api
import os


app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(12)
api = Api(app)
Session(app)


class Registration(Resource):
    def post(self):
        credentials = request.get_json()
        username = credentials['username']
        password = credentials['password']

        if password_check(password):
            if insert_new_user(username, password):
                return {'username': username}, 201
            else:
                return {'error': 'User Exists'}, 409
        else:
            return {'error': 'Invalid Password'}, 500


class Login(Resource):
    def post(self):
        credentials = request.get_json()
        username = credentials['username']
        password = credentials['password']

        if check_credentials(username, password):
            return {"Message": "Login Successful"}, 200
        else:
            return {'error': 'Login Unsuccessful'}, 401


class Logout(Resource):
    def post(self):
       session.clear()


class Chat(Resource):
    def post(self, receiver):
        data = request.get_json()
        message = data['message']
        send_message(receiver, message)

    def get(self, receiver, sender):
        pass


api.add_resource(Registration, '/register')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Chat, '/chat/<string:receiver>')

