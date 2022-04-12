import pymysql
from .secret import *
from flask import request
from flask_restx import Resource
from flask_restx import Namespace

Users = Namespace('Users')
Login = Namespace('Login')

def connect_database():
    conn = pymysql.connect(host=db_host, port=db_port, user=db_user, password=db_password, db=db, charset='utf8')
    db_cursor = conn.cursor()
    return conn, db_cursor

def disconnect_database(conn):
    conn.close()

def argument_check(json_argument):
    for value in json_argument.values():
        if len(value) < 1:
            return False

    return True

@Login.route('')
class LoginApi(Resource):
    def post(self):
        try:
            json_argument = request.get_json()
            self.app_id = json_argument["app_id"]
            self.app_pw = json_argument["app_pw"]
            if not argument_check(json_argument):
                raise()
        except:
            return {"message": "invalid request argument"}, 400

        return self.loginCheck()

    def loginCheck(self):
        conn, db_cursor = connect_database()
        sql_query = f'SELECT * FROM app_users WHERE app_id="{self.app_id}" and app_pw=SHA1("{self.app_pw}")'
        db_cursor.execute(sql_query)
        
        if len(db_cursor.fetchall()) < 1:
            return {"message": "auth fail"}, 404

        disconnect_database(conn)

        return {"message": "auth success"}, 200


# TODO
# * Add email regex check
@Users.route('')
class UserApi(Resource):
    def post(self):
        try:
            json_argument = request.get_json()
            self.app_id = json_argument["app_id"]
            self.app_pw = json_argument["app_pw"]
            self.app_email = json_argument["app_email"]
            if not argument_check(json_argument):
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
        try:
            json_argument = request.get_json()
            self.app_id = json_argument["app_id"]
            self.app_pw = json_argument["app_pw"]
            if not argument_check(json_argument):
                raise()
        except:
            return {"message": "invalid request argument"}, 400

        return self.deleteUser()

    def deleteUser(self):
        conn, db_cursor = connect_database()
        sql_query = f'DELETE FROM app_users WHERE app_id="{self.app_id}" and app_pw=SHA1("{self.app_pw}")'
        try:
            if not db_cursor.execute(sql_query):
                raise()
            conn.commit()
        except:
            disconnect_database(conn)
            return {"message": "delete user fail"}, 400
        disconnect_database(conn)
        return {"message": "delete user success"}, 200
