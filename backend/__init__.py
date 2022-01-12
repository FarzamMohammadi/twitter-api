from flask import Flask
from flask_restful import Resource, Api
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')

