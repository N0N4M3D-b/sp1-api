import sys
import pymysql
import json
import time
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

        sql_query = f'SELECT * FROM app_users WHERE app_id="{self.app_id}"'
        db_cursor.execute(sql_query)

        if len(db_cursor.fetchall()) < 1:
            return {"message": "invalid app user"}, 400

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

@Otts.route('/info/<int:idx>')
class OttInfoAPI(Resource):
    def get(self, idx):
        data = self.GetData(idx)

        if data == None:
            return {"message": "invalid index"}, 404

        member = self.GetMember(idx)

        members = []
        for mem in member:
            mem_info = []
            mem_info.append(mem[0])
            mem_info.append(mem[1])
            members.append(mem_info)

        print(f"TYPE: {data[6]}, {type(data[6])}", flush=True)

        info = {
                    "idx": data[0],
                    "ott": data[1],
                    "account": {
                        "id": data[2],
                        "pw": data[3],
                        "payment": {
                            "type": data[4],
                            "detail": data[5],
                            "next": data[6]
                        },
                        "membership": {
                            "type": data[7],
                            "cost": data[8]
                        }
                    },
                    "updatetime": data[9],
                    "members": members
                }


        return {"message": "get info success", "info": info}, 200

    def GetData(self, idx):
        conn, db_cursor = connect_database()
        sql_query = f'SELECT * FROM ott_users WHERE idx={idx}'
        db_cursor.execute(sql_query)
        data = db_cursor.fetchone()
        disconnect_database(conn)

        return data

    def GetMember(self, idx):
        conn, db_cursor = connect_database()
        sql_query = f'SELECT app_id, isAdmin FROM ott_group WHERE idx={idx}'
        db_cursor.execute(sql_query)
        member = db_cursor.fetchall()
        disconnect_database(conn)

        return member


    def put(self, idx):
        arg_types = {"ott_pw": str, "payment_type": int, "payment_next": int, "membership_type": int, "membership_cost": int}

        try:
            json_argument = request.get_json()

            if "payment_detail" in json_argument.keys():
                arg_types["payment_detail"] = str
                self.payment_detail = json_argument["payment_detail"]
            else:
                self.payment_detail = None

            self.ott_pw = json_argument["ott_pw"]
            self.payment_type = json_argument["payment_type"]
            self.payment_next = json_argument["payment_next"]
            self.membership_type = json_argument["membership_type"]
            self.membership_cost = json_argument["membership_cost"]

            if not Argument(json_argument, arg_types).argument_check():
                raise()
        except Exception as e:
            print(f'{e}', flush=True)
            return {"message": "invalid request argument"}, 400

        if self.CheckIdx(idx) == False:
            return {"message": "invalid index"}, 404

        self.update_time = int(time.time())
        self.UpdateOttAccount(idx)

        return {"message": "update account info success"}, 200

    def UpdateOttAccount(self, idx):
        conn, db_cursor = connect_database()

        if self.payment_detail == None:
            sql_query = f'UPDATE ott_users SET ott_pw="{self.ott_pw}", payment_type="{self.payment_type}", payment_detail=NULL, payment_next="{self.payment_next}", membership_type={self.membership_type}, membership_cost={self.membership_cost}, update_time="{self.update_time}" WHERE idx={idx}'
        else:
            sql_query = f'UPDATE ott_users SET ott_pw="{self.ott_pw}", payment_type="{self.payment_type}", payment_detail="{self.payment_detail}", payment_next="{self.payment_next}", membership_type={self.membership_type}, membership_cost={self.membership_cost}, update_time="{self.update_time}" WHERE idx={idx}'

        db_cursor.execute(sql_query)
        conn.commit()
        disconnect_database(conn)
        
    def CheckIdx(self, idx):
        conn, db_cursor = connect_database()
        sql_query = f'SELECT * FROM ott_users WHERE idx = {idx}'
        db_cursor.execute(sql_query)
        isValid = db_cursor.fetchone()
        disconnect_database(conn)

        if isValid == None:
            return False
        else:
            return True




