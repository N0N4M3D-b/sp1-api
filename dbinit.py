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
        self.check_table('app_users', self.create_user_table)
        self.check_table('otts', self.create_ott_table)
        self.check_table('ott_users', self.create_ott_user_table)
        self.check_table('ott_group', self.create_group_table)
        self.init_ott_table()
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


    def check_table(self, table_name, func):
        self.db_cursor.execute(self.select_table_query(table_name))

        if (len(self.db_cursor.fetchall()) < 1):
            func()
            print(f'[*] create {table_name} table')
            

    def create_user_table(self):
        sql_query = '''
                    CREATE TABLE app_users (
                        app_id varchar(20) NOT NULL PRIMARY KEY,
                        app_pw varchar(50) NOT NULL,
                        app_email varchar(50) NOT NULL
                    )
                    '''
        self.db_cursor.execute(sql_query)

    
    def create_ott_table(self):
        sql_query = '''
                    CREATE TABLE otts (
                        ott varchar(20) NOT NULL PRIMARY KEY
                    )
                    '''
        self.db_cursor.execute(sql_query)


    def init_ott_table(self):
        ott_service = ['netflix', 'wavve']

        for service in ott_service:
            sql_query = f'SELECT * FROM otts WHERE ott="{service}"'
            if not self.db_cursor.execute(sql_query):
                sql_query = f'''
                            INSERT INTO otts VALUES ("{service}")
                            '''
                self.db_cursor.execute(sql_query) 


    def create_ott_user_table(self):
        sql_query = '''
                    CREATE TABLE ott_users (
                        idx INT NOT NULL AUTO_INCREMENT,
                        ott varchar(20) NOT NULL,
                        ott_id varchar(20) NOT NULL,
                        ott_pw varchar(50) NOT NULL,
                        payment_type INT,
                        payment_detail varchar(20),
                        payment_next DATETIME,
                        membership_type INT,
                        membership_cost INT,
                        update_time DATETIME,
                        member_count INT NOT NULL,
                        PRIMARY KEY (idx),
                        UNIQUE KEY (ott_id, ott),
                        FOREIGN KEY (ott) REFERENCES otts (ott) ON DELETE CASCADE 
                    )
                    '''
        self.db_cursor.execute(sql_query)


    def create_group_table(self):
        sql_query = '''
                    CREATE TABLE ott_group (
                        app_id varchar(20) NOT NULL,
                        idx INT NOT NULL,
                        isAdmin INT NOT NULL,
                        PRIMARY KEY (app_id, idx),
                        FOREIGN KEY (app_id) REFERENCES app_users (app_id) ON DELETE CASCADE,
                        FOREIGN KEY (idx) REFERENCES ott_users (idx) ON DELETE CASCADE
                    )
                    '''
        self.db_cursor.execute(sql_query)


InitTable()
