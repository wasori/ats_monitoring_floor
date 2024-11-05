# -*- coding: utf-8 -*-

import pymysql
import json

class globalDB:
    connecter = ""  # type: ignore
    cursors = ""

    def connecter(self):
        try:
            self.connecter = pymysql.connect(
                host="1.220.178.46",
                port=3306,
                user="atsol",
                passwd="1234",
                db="minam",
                charset="utf8",
                # autocommit=True
            )
            self.cursors = self.connecter.cursor()
            # print("DB connected successfully")
        except pymysql.MySQLError as e:
            print(f"Error connecting to MySQL: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def signin(self, values):

        quarry = ""
        receive = ""
        result = ""

        jsonvalue = values
        print("Received values:", jsonvalue)

        quarry = (
            f"SELECT hos_name FROM admin_info_tb WHERE id='{jsonvalue['id']}' AND pw='{jsonvalue['pw']}'"
        )

        if self.cursors == "":
            print("DB not connect")
            return
        else:
            self.cursors.execute(quarry)  # type: ignore
            receive = self.cursors.fetchall()  # type: ignore

        if not receive:  # type: ignore
            return {"result": 0}
        else:
            hospital_name = receive[0]  # 조회된 hospital_name
        return {"result": 1, "hospital_name": hospital_name}