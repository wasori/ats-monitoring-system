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

    def insert_temp(self, values):

        json_value = json.loads(values)

        quarry = ""
        quarry = "insert into temp_tb(robot_id,hospital_name,x,y,yaw,img_width,img_height,temperature,personid,snapshot,uptime) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,CURRENT_TIMESTAMP)"

        robot_id = json_value["robot_id"]
        hospital_name = json_value["hospital_name"]
        x = json_value["x"]
        y = json_value["y"]
        yaw = json_value["yaw"]
        img_width = json_value["img_width"]
        img_height = json_value["img_height"]
        temperature = json_value["temperature"]
        personid = json_value["personid"]
        snapshot = json_value["snapshot"]

        arr = (
            robot_id,
            hospital_name,
            x,
            y,
            yaw,
            img_width,
            img_height,
            temperature,
            personid,
            snapshot,
        )

        try:
            self.cursors.execute(quarry, arr)
            self.connecter.commit()
        except Exception as e:
            print(f"Error inserting data: {e}")
            self.connecter.rollback()

    # 온도체크 사진 결과 가져오기
    def select_temp(self):
        quarry = ""
        receive = ""
        items = []

        quarry = "SELECT * FROM temp_tb ORDER BY uptime DESC LIMIT 1"

        if self.cursors == "":
            print("DB not connect")
            return
        else:
            self.cursors.execute(quarry)  # type: ignore
            receive = self.cursors.fetchall()

            if receive:
                row = receive[0]
                items.append(
                    {
                        "robot_id": row[0],
                        "hos_name": row[1],
                        "x": row[2],
                        "y": row[3],
                        "yaw": row[4],
                        "img_width": row[5],
                        "img_height": row[6],
                        "temperature": row[7],
                        "personid": row[8],
                        "snapshot": row[9],
                        "uptime": row[10],
                    }
                )

        jsondata = json.dumps(items, default=str)
        return jsondata

    def select_all_temp(self):
        quarry = ""
        receive = ""
        items = []

        quarry = "SELECT * FROM temp_tb"

        if self.cursors == "":
            print("DB not connect")
            return
        else:
            self.cursors.execute(quarry)  # type: ignore
            receive = self.cursors.fetchall()

            for row in receive:
                items.append(
                    {
                        "robot_id": row[0],
                        "hos_name": row[1],
                        "x": row[2],
                        "y": row[3],
                        "yaw": row[4],
                        "img_width": row[5],
                        "img_height": row[6],
                        "temperature": row[7],
                        "personid": row[8],
                        "snapshot": row[9],
                        "uptime": row[10],
                    }
                )

        jsondata = json.dumps(items, default=str)
        return jsondata

    def insert_sensor(self, values):

        json_value = json.loads(values)

        quarry = ""
        quarry = "insert into sensor_data_tb(rid,xaxis,yaxis,dust,water,fire,uptime,hos_name) values(%s,%s,%s,%s,%s,%s,CURRENT_TIMESTAMP,%s)"

        rid = json_value["robot_id"]
        dust = round(float(json_value["dust(ug)"]), 2)
        water = json_value["waterDetect"]
        fire = json_value["FireDetect"]
        # distance = json_value["distance"]
        xaxis = json_value["x"]
        yaxis = json_value["y"]
        hos_name = json_value["hospital_name"]

        arr = (rid, xaxis, yaxis, dust, water, fire, hos_name)

        if self.cursors == "":
            print("DB not connect")
            self.connecter.rollback()  # type: ignore
            return
        else:
            self.cursors.execute(quarry, arr)  # type: ignore
            self.connecter.commit()  # type: ignore

    def select_all_sensor(self):
        quarry = ""
        receive = ""
        items = []

        quarry = "SELECT * FROM sensor_data_tb"

        if self.cursors == "":
            print("DB not connect")
            return
        else:
            self.cursors.execute(quarry)  # type: ignore
            receive = self.cursors.fetchall()

            for row in receive:
                items.append(
                    {
                        "robot_id": row[1],  # rid
                        "x": row[2],  # xaxis
                        "y": row[3],  # yaxis
                        "dust": row[4],  # dust
                        "water": row[5],  # water
                        "fire": row[6],  # fire
                        "uptime": row[7],  # uptime
                        "hos_name": row[8],  # hos_name
                    }
                )

        jsondata = json.dumps(items, default=str)
        return jsondata

    def insert_vision(self, values):

        json_value = json.loads(values)

        quarry = ""
        quarry = "insert into vision_data_tb(rid,room,sickbed,pose,down,uptime,hos_name) values(%s,%s,%s,%s,%s,CURRENT_TIMESTAMP,%s)"

        downval = 0

        rid = json_value["robot_id"]
        patient = json_value["patient_no"]
        pose = json_value["pose"]
        down = json_value["falldown"]
        hos_name = json_value["hospital_name"]

        roombed = patient.split("-")

        if down == "true":
            downval = 1

        arr = (rid, roombed[0], roombed[1], pose, downval, hos_name)

        if self.cursors == "":
            print("DB not connect")
            self.connecter.rollback()  # type: ignore
            return
        else:
            self.cursors.execute(quarry, arr)  # type: ignore
            self.connecter.commit()  # type: ignore

    def select_all_vision(self):
        quarry = ""
        receive = ""
        items = []

        quarry = "SELECT * FROM vision_data_tb"

        if self.cursors == "":
            print("DB not connect")
            return
        else:
            self.cursors.execute(quarry)  # type: ignore
            receive = self.cursors.fetchall()

            for row in receive:
                items.append(
                    {
                        "robot_id": row[1],
                        "room": row[2],
                        "sickbed": row[3],
                        "pose": row[4],
                        "down": row[5],
                        "uptime": row[6],
                        "hos_name": row[7],
                    }
                )

        jsondata = json.dumps(items, default=str)
        return jsondata

    def insert_robot(self, values):
        json_value = json.loads(values)

        quarry = ""
        quarry = "insert into robot_data_tb(rid,xaxis,yaxis,uptime) values(%s,%s,%s,CURRENT_TIMESTAMP)"

        rid = json_value["robot_id"]

        if rid == "" or rid == "/":
            rid = "MR04"

        xaxis = json_value["x"]
        yaxis = json_value["y"]
        # hos_name = json_value["hospital_name"]
        # yaw = 90

        arr = (rid, xaxis, yaxis)

        if self.cursors == "":
            print("DB not connect")
            self.connecter.rollback()  # type: ignore
            return

        else:
            self.cursors.execute(quarry, arr)  # type: ignore
            self.connecter.commit()  # type: ignore

    def select_all_robot(self):
        quarry = ""
        receive = ""
        items = []

        quarry = "SELECT * FROM robot_data_tb"

        if self.cursors == "":
            print("DB not connect")
            return
        else:
            self.cursors.execute(quarry)  # type: ignore
            receive = self.cursors.fetchall()

            for row in receive:
                items.append(
                    {
                        "robot_id": row[1],
                        "xaxis": row[2],
                        "yaxis": row[3],
                        "uptime": row[4],
                        "hos_name": row[5],
                    }
                )

        jsondata = json.dumps(items, default=str)
        return jsondata

    def signin(self, values):

        quarry = ""
        receive = ""
        result = ""

        jsonvalue = values

        quarry = (
            f"select hos_name from admin_info_tb where id='"
            + jsonvalue["id"]
            + "' AND pw='"
            + jsonvalue["pw"]
            + "'"
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

    def select_hos(self, hospital_name, ward):
        quarry = ""
        receive = ""
        result = ""

        # 쿼리문 생성: 병원 이름과 병동 조건
        quarry = f"SELECT COUNT(*) FROM hospital_tb WHERE hospital_name='{hospital_name}' AND ward='{ward}'"

        if self.cursors == "":
            print("DB not connect")
            return
        else:
            self.cursors.execute(quarry)  # 쿼리 실행
            receive = self.cursors.fetchall()  # 결과 가져오기

        if not receive:
            result = 0
        else:
            result = receive[0][0]  # 쿼리 결과 값 가져오기

        return result

    def select_robot_regist(self, hospital_name, ward):
        # SQL 쿼리 작성
        query = f"""
        SELECT 
            COUNT(*) AS total_count,
            SUM(CASE WHEN state = '운행' THEN 1 ELSE 0 END) AS operating_count,
            SUM(CASE WHEN state = '고장' THEN 1 ELSE 0 END) AS broken_count,
            SUM(CASE WHEN state = '수리' THEN 1 ELSE 0 END) AS repair_count
        FROM 
            robot_regist_tb
        WHERE 
            hospital_name = '{hospital_name}'
            AND ward = '{ward}'
        """

        # 쿼리 실행
        self.cursors.execute(query)
        receive = self.cursors.fetchone()  # 결과는 한 줄만 반환

        # 결과를 딕셔너리로 반환
        return {
            "total_count": int(receive[0]),  # 카운트는 정수로 변환
            "operating_count": (
                int(receive[1]) if receive[1] is not None else 0
            ),  # None이면 0.0으로 설정
            "broken_count": (
                int(receive[2]) if receive[2] is not None else 0
            ),  # None이면 0.0으로 설정
            "repair_count": (
                int(receive[3]) if receive[3] is not None else 0
            ),  # None이면 0.0으로 설정
        }

    def select_robot_regist_all(self, hospital_name):

        quarry = ""
        receive = ""
        items = []

        # SQL 쿼리 작성
        query = f"""
        SELECT * FROM robot_regist_tb
        WHERE hospital_id = '{hospital_name}'
        """

        if self.cursors == "":
            print("DB not connect")
            return
        else:
            # 쿼리 실행 및 결과 가져오기
            self.cursors.execute(query)
            receive = self.cursors.fetchall()

            for row in receive:
                items.append(
                    {
                        "robot_id": row[0],
                        "ward": row[2],
                        "room": row[3],
                        "uptime": row[5],
                    }
                )

        jsondata = json.dumps(items, ensure_ascii=False, default=str)
        return jsondata

    def select_total_alert(self):

        quarry = ""
        receive = ""
        items = []

        # SQL 쿼리 작성
        query = f"""
        SELECT * FROM total_alert_tb
        """

        if self.cursors == "":
            print("DB not connect")
            return
        else:
            # 쿼리 실행 및 결과 가져오기
            self.cursors.execute(query)
            receive = self.cursors.fetchall()

            for row in receive:
                items.append(
                    {
                        "content": row[0] if row[0] is not None else "-",
                        "robot_id": row[1] if row[1] is not None else "-",
                        "place": row[2] if row[2] is not None else "-",
                        "uptime": row[3] if row[3] is not None else "-",
                        "name": row[4] if row[4] is not None else "-",
                        "name_value": row[5] if row[5] is not None else "-",
                        "blank": row[6] if row[6] is not None else "-",
                        "blank2": row[7] if row[7] is not None else "-",
                    }
                )

        jsondata = json.dumps(items, ensure_ascii=False, default=str)
        return jsondata

    def get_alarm_data(self, hospital_name):

        query = ""
        receive = ""
        items = []

        # SQL 쿼리 작성
        query = f"""
            SELECT * FROM alarm_data_tb
            WHERE hos_name = '{hospital_name}'
            """

        if self.cursors == "":
            print("DB not connect")
            return
        else:
            # 쿼리 실행 및 결과 가져오기
            self.cursors.execute(query)
            receive = self.cursors.fetchall()

            for row in receive:
                items.append(
                    {
                        "robot_id": row[1],
                        "x": row[2],
                        "y": row[3],
                        "content": row[4],
                        "value": row[5],
                        "uptime": row[7],
                        "name": row[8],
                        "comment": row[9],
                        "blank": row[10],
                        "blank2": row[11],
                    }
                )

        jsondata = json.dumps(items, ensure_ascii=False, default=str)
        return jsondata

    def get_robot_info(self, robot_id):

        query = "SELECT ward, room FROM robot_regist_tb WHERE robot_id = %s"
        self.cursors.execute(query, (robot_id,))
        result = self.cursors.fetchone()  # 튜플 형태로 반환

        if result:  # 결과가 None이 아닐 때만 처리
            return {
                "ward": result[0],
                "room": result[1],
            }  # 딕셔너리 형태로 변환하여 반환
        return None  # 결과가 없을 경우 None 반환

    def get_image_url(self, hospital_name, floor):
        query = (
            "SELECT url FROM hospital_images WHERE hospital_name = %s AND floor = %s"
        )
        self.cursors.execute(query, (hospital_name, floor))
        result = self.cursors.fetchone()  # 튜플 형태로 반환

        if result:  # 결과가 None이 아닐 때만 처리
            return result[0]  # URL 반환
        return None  # 결과가 없을 경우 None 반환

    # 데이터베이스 메서드


    def get_images(self, hospital_name):
        query = "SELECT url, floor FROM hospital_images WHERE hospital_name = %s"
        self.cursors.execute(query, (hospital_name,))
        result = self.cursors.fetchall()
    
        if result:
            return [{'url': row[0], 'floor': row[1]} for row in result]  # URL과 floor 값을 딕셔너리로 반환
        return []

    def insert_total_alert(
        self, content, robot_id, place, uptime, name, name_value, blank, blank2
    ):
        # 알림 데이터를 total_alert_tb 테이블에 삽입하는 SQL 쿼리
        query = """
        INSERT INTO total_alert_tb (content, robot_id, place, uptime, name, name_value, blank, blank2)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        try:
            self.cursors.execute(
                query,
                (content, robot_id, place, uptime, name, name_value, blank, blank2),
            )
            self.connecter.commit()  # 변경사항 저장
        except Exception as e:
            print(f"Error inserting data: {e}")
            self.connecter.rollback()  # 오류 발생 시 롤백

    def insert_alarm(self, values):
        json_value = json.loads(values)

        quarry = ""
        quarry = "insert into alarm_data_tb(rid,xaxis,yaxis,content,uptime,hos_name"

        rid = json_value["rid"]
        xaxis = json_value["xaxis"]
        yaxis = json_value["yaxis"]
        content = json_value["content"]
        value = json_value["value"]
        hos_name = json_value["hos_name"]

        arr = ""

        if json_value["value"] != "":
            quarry += ",value) values(%s,%s,%s,%s,CURRENT_TIMESTAMP,%s,%s)"
            arr = (rid, xaxis, yaxis, content, hos_name, value)
        else:
            quarry += ") values(%s,%s,%s,%s,CURRENT_TIMESTAMP,%s)"
            arr = (rid, xaxis, yaxis, content, hos_name)

        if self.cursors == "":
            print("DB not connect")
            self.connecter.rollback()  # type: ignore
            return
        else:
            self.cursors.execute(quarry, arr)  # type: ignore
            self.connecter.commit()  # type: ignore
