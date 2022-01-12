from .login import check_credentials
from .register import insert_new_user, password_check, hash_password
from .chat import send_message, check_unread_msgs
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
                return {'Error': 'User Exists'}, 409
        else:
            return {'Error': 'Invalid Password'}, 500


class Login(Resource):
    def post(self):
        credentials = request.get_json()
        username = credentials['username']
        password = credentials['password']

        if check_credentials(username, password):
            return {"Message": "Login Successful"}, 200
        else:
            return {'Error': 'Login Unsuccessful'}, 401


class Logout(Resource):
    def post(self):
       session.clear()


class Chat(Resource):
    def post(self, username):
        data = request.get_json()
        message = data['message']
        receiver = username
        if send_message(username, message):
            return {"Message": "Message Sent"}, 200
        else:
            return {"Error": "Message Could Not Be Sent"}, 401

    def get(self, username):
        sender = username
        data = check_unread_msgs(sender)
        if data:
            return data, 200
        else:
            return {"Error": "No Message Found"}, 401


class Tweet(Resource):
    def post(self):
        data = request.get_json()
        message = data['message']


    def get(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


api.add_resource(Registration, '/register')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Chat, '/chat/<string:username>')
api.add_resource(Chat, '/tweet')

