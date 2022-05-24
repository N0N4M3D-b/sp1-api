from flask import Flask
from flask_restx import Api
from dbinit import *
from api.users import Users
from api.users import Login
from api.otts import Otts
from api.secret import *

InitTable()
app = Flask(__name__)
api = Api(app)

api.add_namespace(Users, '/users')
api.add_namespace(Login, '/login')
api.add_namespace(Otts, '/otts')

if __name__ == '__main__':
    app.run(debug=True, host=app_host, port=app_port)
