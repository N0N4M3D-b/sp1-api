import pymysql
import os
from api.secret import *

class InitTable:
    def __init__(self):
        self.conn = pymysql.connect(host=db_host, port=db_port, user=db_root, password=db_root_password, db=mysql, charset='utf8')
        self.db_cursor = self.conn.cursor()
        self.create_project_user()
        self.conn.commit()
        self.conn.close()

        self.conn = pymysql.connect(host=db_host, port=db_port, user=db_user, password=db_password, db=db, charset='utf8')
        self.db_cursor = self.conn.cursor()
        self.check_user_table()
        self.conn.commit()
        self.conn.close()


    def create_project_user(self):
        if self.db_cursor.execute('SELECT user FROM user WHERE user="sp1"'):
            return
        self.db_cursor.execute('CREATE DATABASE sp1 DEFAULT CHARACTER SET utf8')
        self.db_cursor.execute('CREATE USER "sp1"@"%" IDENTIFIED BY "user_passwd"')
        self.db_cursor.execute('GRANT ALL PRIVILEGES ON sp1.* TO "sp1"@"%"')


    def select_table_query(self, table_name):
        sql_query = f'SELECT * FROM information_schema.columns WHERE table_schema="sp1" and table_name="{table_name}"'
        return sql_query


    def check_user_table(self):
        self.db_cursor.execute(self.select_table_query('app_users'))

        if (len(self.db_cursor.fetchall()) < 1):
            self.create_user_table()
            print('[*] create user table')
            

    def create_user_table(self):
        sql_query = '''
                    CREATE TABLE app_users (
                        app_id varchar(20) NOT NULL PRIMARY KEY,
                        app_pw varchar(50) NOT NULL,
                        app_email varchar(50) NOT NULL
                    )
                    '''
        self.db_cursor.execute(sql_query)


InitTable()
