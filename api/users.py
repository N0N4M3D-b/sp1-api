import pymysql
from .secret import *
from .api_util import *
from flask import request
from flask_restx import Resource
from flask_restx import Namespace

Users = Namespace('Users')
Login = Namespace('Login')

@Login.route('')
class LoginApi(Resource):
    def post(self):
        arg_types = {"app_id": str, "app_pw": str}
        try:
            json_argument = request.get_json()
            self.app_id = json_argument["app_id"]
            self.app_pw = json_argument["app_pw"]

            if not Argument(json_argument, arg_types).argument_check():
                raise()
        except:
            return {"message": "invalid request argument"}, 400

        return self.loginCheck()

    def loginCheck(self):
        conn, db_cursor = connect_database()
        sql_query = f'SELECT * FROM app_users WHERE app_id="{self.app_id}" and app_pw=SHA1("{self.app_pw}")'
        db_cursor.execute(sql_query)
        
        if len(db_cursor.fetchall()) < 1:
            disconnect_database(conn)
            return {"message": "auth fail"}, 404

        disconnect_database(conn)

        return {"message": "auth success"}, 200


@Users.route('')
class UserApi(Resource):
    def post(self):
        arg_types = {"app_id": str, "app_pw": str, "app_email": str}
        try:
            json_argument = request.get_json()
            self.app_id = json_argument["app_id"]
            self.app_pw = json_argument["app_pw"]
            self.app_email = json_argument["app_email"]
            
            if not Argument(json_argument, arg_types).argument_check():
                raise()
        except:
            return {"message": "invalid request argument"}, 400

        return self.insertUser()

    def insertUser(self):
        conn, db_cursor = connect_database()
        sql_query = f'''
                    INSERT INTO app_users VALUES (
                        "{self.app_id}", SHA1("{self.app_pw}"), "{self.app_email}"
                    )
                    '''
        try:
            db_cursor.execute(sql_query)
            conn.commit()
        except:
            disconnect_database(conn)
            return {"message": "already exist id"}, 401
        disconnect_database(conn)
        return {"message": "insert user success"}, 201


    def delete(self):
        arg_types = {"app_id": str, "app_pw": str}
        try:
            json_argument = request.get_json()
            self.app_id = json_argument["app_id"]
            self.app_pw = json_argument["app_pw"]
            if not Argument(json_argument, arg_types).argument_check():
                raise()
        except:
            return {"message": "invalid request argument"}, 400

        return self.deleteUser()

    def deleteUser(self):
        conn, db_cursor = connect_database()
        sql_query = f'DELETE FROM app_users WHERE app_id="{self.app_id}" AND app_pw=SHA1("{self.app_pw}")'
        try:
            if not db_cursor.execute(sql_query):
                raise()
            conn.commit()
        except:
            disconnect_database(conn)
            return {"message": "delete user fail"}, 401
        disconnect_database(conn)
        return {"message": "delete user success"}, 200


    def put(self):
        arg_types = {"app_id": str, "app_pw": str, "app_email": str}
        try:
            json_argument = request.get_json()
            self.app_id = json_argument["app_id"]
            self.app_pw = json_argument["app_pw"]
            self.app_email = json_argument["app_email"]
            if not Argument(json_argument, arg_types).argument_check():
                raise()
        except:
            return {"message": "invalid request argument"}, 400

        return self.modifyUser()

    def modifyUser(self):
        conn, db_cursor = connect_database()
        sql_query = f'UPDATE app_users SET app_id="{self.app_id}", app_pw=SHA1("{self.app_pw}") WHERE app_id="{self.app_id}"'
        try:
            if not db_cursor.execute(sql_query):
                raise()
            conn.commit()
        except:
            disconnect_database(conn)
            return {"message": "modify user info fail"}, 400
        disconnect_database(conn)
        return {"message": "modify user info success"}, 200
