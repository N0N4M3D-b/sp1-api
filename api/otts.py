import sys
import pymysql
from .secret import *
from .api_util import *
from flask import request
from flask_restx import Resource
from flask_restx import Namespace

Otts = Namespace('Otts')

@Otts.route('/group')
class OttUserAPI(Resource):
    def post(self):
        arg_types = {"app_id": str, "ott_id": str, "ott_pw": str, "ott": str}
        try:
            json_argument = request.get_json()
            self.app_id = json_argument["app_id"]
            self.ott_id = json_argument["ott_id"]
            self.ott_pw = json_argument["ott_pw"]
            self.ott = json_argument["ott"]

            if not Argument(json_argument, arg_types).argument_check():
                raise()
        except:
            return {"message": "invalid request argument"}, 400
 
        return self.InsertOttUser(self.GetOttUserIdx())

    def InsertOttUser(self, idx):
        conn, db_cursor = connect_database()
        if idx == -1:
            sql_query = f'''
                        INSERT INTO ott_users VALUES (
                            NULL,
                            "{self.ott}",
                            "{self.ott_id}", 
                            "{self.ott_pw}", 
                            NULL,
                            NULL,
                            NULL,
                            NULL,
                            NULL,
                            NULL,
                            1
                        )
                        '''
            try:
                db_cursor.execute(sql_query) 
                conn.commit()
            except:
                disconnect_database(conn)
                return {"message": "invalid ott service"}, 400
            idx = self.GetOttUserIdx()
            self.InsertOttGroup(idx, 1)    
        else:
            sql_query = f'SELECT * FROM ott_group WHERE app_id="{self.app_id}" AND idx={idx}'
            db_cursor.execute(sql_query)
            if len(db_cursor.fetchall()) != 0:
                return {"message": "already joined in group"}, 401

            sql_query = f'UPDATE ott_users SET member_count = member_count + 1 WHERE idx={idx}'
            db_cursor.execute(sql_query)
            conn.commit()

            self.InsertOttGroup(idx, 0)

        disconnect_database(conn)
        return {"message": "joined in group", "idx": idx}, 200

    def InsertOttGroup(self, idx, isAdmin):
        conn, db_cursor = connect_database()
        sql_query = f'''
                        INSERT INTO ott_group VALUES (
                            "{self.app_id}",
                            {idx},
                            {isAdmin}
                        )
                    '''
        db_cursor.execute(sql_query)
        conn.commit()
        disconnect_database(conn)

    def GetOttUserIdx(self):
        conn, db_cursor = connect_database()
        sql_query = f'SELECT idx FROM ott_users WHERE ott_id="{self.ott_id}" AND ott_pw="{self.ott_pw}" AND ott="{self.ott}"'
        db_cursor.execute(sql_query)
        idx = db_cursor.fetchall()

        disconnect_database(conn)

        if len(idx) != 1:
            return -1
        else:
            return idx[0][0]


    def delete(self):
        arg_types = {"app_id": str, "idx": int}
        try:
            json_argument = request.get_json()
            self.app_id = json_argument["app_id"]
            self.idx = json_argument["idx"]

            if not Argument(json_argument, arg_types).argument_check():
                raise()
        except:
            return {"message": "invalid request argument"}, 400

        conn, db_cursor = connect_database()
        sql_query = f'SELECT isAdmin FROM ott_group WHERE app_id="{self.app_id}" AND idx={self.idx}'
        db_cursor.execute(sql_query)
        try:
            isAdmin = db_cursor.fetchone()[0]
        except:
            return {"message": "invalid index"}, 404
        disconnect_database(conn)

        if isAdmin == 1:
            self.DeleteGroup() 
        else:
            self.DeleteGroupUser()

        return {"message": "exit group successfully"}, 200

    def DeleteGroup(self):
        conn, db_cursor = connect_database()
        sql_query = f'DELETE FROM ott_users WHERE idx={self.idx}'
        db_cursor.execute(sql_query)
        conn.commit()
        disconnect_database(conn)

    def DeleteGroupUser(self):
        conn, db_cursor = connect_database()
        sql_query = f'DELETE FROM ott_group WHERE app_id="{self.app_id}" AND idx={self.idx}'
        db_cursor.execute(sql_query)
        sql_query = f'UPDATE ott_users SET member_count = member_count - 1 WHERE idx={self.idx}'
        db_cursor.execute(sql_query)
        conn.commit()
        disconnect_database(conn)

@Otts.route('/info')
class OttInfoAPI(Resource):
    def get(self):
        pass


    def put(self):
        pass
