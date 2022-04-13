import pymysql
from .secret import *

def connect_database():
    conn = pymysql.connect(host=db_host, port=db_port, user=db_user, password=db_password, db=db, charset='utf8')
    db_cursor = conn.cursor()
    return conn, db_cursor

def disconnect_database(conn):
    conn.close()

class Argument():
    def __init__(self, json_argument, argument_types):
        self.json_argument = json_argument
        self.argument_types = argument_types

    def argument_check(self):
        if not self.argument_length_check():
            return False

        if not self.argument_type_check():
            return False

        return True

    def argument_length_check(self):
        for value in self.json_argument.values():
            if len(value) < 1:
                return False

        return True

    def argument_type_check(self):
        for arg_key in self.argument_types.keys():
            if not type(self.json_argument[arg_key]) is self.argument_types[arg_key]:
                return False
            
        return True
