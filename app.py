# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template, url_for, g, request, send_from_directory, abort
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt
import time
import json
import threading
import database as base

mqtt_data = {}
app = Flask(__name__, static_url_path='', static_folder='static')
socketio = SocketIO(app)


# 메시지 수신 핸들러
def on_message(client, userdata, message):
    global db
    global sensor

    if message.topic == "ros_thermocam":
        db = base.globalDB()
        db.connecter()
        result = db.insert_temp(message.payload)
    
    elif message.topic == "sensor":
        message_payload = message.payload.decode('utf-8')  # 바이트를 문자열로 변환
        # print(message_payload)  # 디코딩된 메시지 확인

        jsonmsg = json.loads(message_payload)
        db = base.globalDB()
        db.connecter()

        db.insert_sensor(message.payload)


        dust = round(float(jsonmsg["dust(ug)"]),2)
        water = int(jsonmsg["waterDetect"])
        fire = int(jsonmsg["FireDetect"])
        xaxis = str(jsonmsg["x"])
        yaxis = str(jsonmsg["y"])
        hos_name = str(jsonmsg["hospital_name"])

        if (jsonmsg["robot_id"] is None) or (not jsonmsg["robot_id"]):
            jsonmsg["robot_id"] = "ZK00"

        if dust>3000 or water == 1 or fire == 1:

            dust_val =str(dust)

            if dust > 3000:
                insertdata = f'{{"rid":"{jsonmsg["robot_id"]}","xaxis":"{xaxis}","yaxis":"{yaxis}","content":"dust","value":"{dust_val}","hos_name":"{hos_name}"}}'
                db.insert_alarm(insertdata)

            if water == 1:
                insertdata = f'{{"rid":"{jsonmsg["robot_id"]}","xaxis":"{xaxis}","yaxis":"{yaxis}","content":"water","value":"1","hos_name":"{hos_name}"}}'
                db.insert_alarm(insertdata)

            if fire == 1:
                insertdata = f'{{"rid":"{jsonmsg["robot_id"]}","xaxis":"{xaxis}","yaxis":"{yaxis}","content":"fire","value":"1","hos_name":"{hos_name}"}}'
                db.insert_alarm(insertdata)

    elif message.topic == "aos_pose_detect_result":
        message_payload = message.payload.decode('utf-8') 
        jsonmsg = json.loads(message.payload)

        db = base.globalDB()
        db.connecter()

        visionjson = db.select_vision_uptime()
        vision = json.loads(visionjson) # type: ignore
        print(vision)

        db.insert_vision(message.payload)

        falldown = str(jsonmsg["falldown"])
        pose_value  = str(jsonmsg["pose"])
        hos_name = str(jsonmsg["hospital_name"])
        roonbed = jsonmsg['patient_no'].split('-')

        

        pose = 0
        down = 0
        check = -1

        # 기존의 데이터베이스에서 `room`과 `sickbed`가 일치하는 항목 찾기
        for i in range(0, len(vision)):
            if vision[i]['room'] == int(roonbed[0]) and vision[i]['sickbed'] == int(roonbed[1]):
                check = i
                break
            
        # pose 상태 확인
        if check != -1:
            if vision[check]['pose'] == pose_value:
                pose = 1  # 포즈가 동일하면 1로 설정
            elif vision[check]['pose'] == "none":
                pose = 0  # 포즈가 없으면 0으로 설정
        else:
            pose = 0

        # pose 또는 falldown 상태에 따라 하나의 insert 문 생성
        if pose == 1 or falldown:
            content = "pose" if pose == 1 else "down"
            value = pose_value if pose == 1 else "1"

            # 하나의 insert 데이터 생성
            insertdata = (
                '{"rid":"'+jsonmsg["robot_id"]+'", "xaxis":"'+str(int(roonbed[0]))+
                '", "yaxis":"'+str(int(roonbed[1]))+'", "content":"'+content+
                '", "value":"'+value+'", "hos_name" : "'+hos_name+'"}'
            )

            print("Insert Data:", insertdata)  # 확인용 출력
            db.insert_alarm(insertdata)  # 한 번만 insert 호출


    elif message.topic == "robot_position":
        message_payload = message.payload.decode('utf-8') 
        jsonmsg = json.loads(message.payload)

        db = base.globalDB()
        db.connecter()
        db.insert_robot(message.payload)
        # 클라이언트에 메시지 전송
        socketio.emit('robot_position', jsonmsg)
        print(jsonmsg)
        
# MQTT 연결 설정
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("ros_thermocam")
    client.subscribe("sensor")
    client.subscribe("robot_position")
    client.subscribe("aos_pose_detect_result")
    client.subscribe("signin")
    

def start_mqtt_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message 

    client.connect("1.220.178.46", 11883, 60)
    
    # MQTT 루프를 비동기로 시작
    client.loop_start()

    return client

####################################################################
####################################################################

# Flask 라우팅
@app.route('/')
def index():
    return render_template('index.html')  # main.html 렌더링

@app.route('/main')
def main():
    return render_template('main.html')  # main.html 렌더링

@app.route('/test')
def test():
    return render_template('test.html')  # main.html 렌더링

####################################################################
####################################################################

@app.route('/send_pose_data', methods=['POST'])
def send_pose_data():
    pose_data = {
        "robot_id": "ZK99",
        "patient_no": "204-3",
        "falldown": False,
        "pose": "up",
        "x": 210,
        "y": 167,
        "hospital_name": "daon"
    }
    client.publish('aos_pose_detect_result', json.dumps(pose_data))
    return "Pose data sent!"

@app.route('/send_sensor_data', methods=['POST'])
def send_sensor_data():
    sensor_data = {
        "dust(ug)": 342,
        "waterDetect": True,
        "FireDetect": True,
        "battery": 253,
        "robot_id": "ZK04",
        "hospital_name": "daon",
        "x": "0.00",
        "y": "0.00"
    }
    client.publish('sensor', json.dumps(sensor_data))
    return "Sensor data sent!"

##################################################################
##################################################################

@app.route('/data', methods=['GET'])
def get_data():
    db = base.globalDB()
    db.connecter()
    result = db.select_temp()
    return result

@app.route('/temp_data', methods=['GET'])
def get_temp_data():
    db = base.globalDB()
    db.connecter()
    result = db.select_all_temp()
    return result

@app.route('/sensor_data', methods=['GET'])
def get_sensor_data():
    db = base.globalDB()
    db.connecter()
    result = db.select_all_sensor()
    return result

@app.route('/vision_data', methods=['GET'])
def get_vision_data():
    db = base.globalDB()
    db.connecter()
    result = db.select_all_vision()
    return result

@app.route('/robot_data', methods=['GET'])
def get_robot_data():
    db = base.globalDB()
    db.connecter()
    result = db.select_all_robot()
    return result

@app.route('/get_hos_data', methods=['GET'])
def get_hos_data():
    ward = request.args.get('ward')
    hospital_name = request.args.get('hospital_name')
    db = base.globalDB()
    db.connecter()
    result = db.select_hos(hospital_name,ward)
    return jsonify({'count': result})

@app.route('/get_robo_regist_data', methods=['GET'])
def get_robo_data():
    ward = request.args.get('ward')
    hospital_name =  request.args.get('hospital_name')
    db = base.globalDB()
    db.connecter()
    result = db.select_robot_regist(hospital_name,ward)
    print(result)
    # JSON 형식으로 결과 반환
    return jsonify({
        'total_count': result['total_count'],
        'operating_count': result['operating_count'],
        'broken_count': result['broken_count'],
        'repair_count': result['repair_count']
    })

@app.route('/get_robo_count_all', methods=['GET'])
def get_robo_count_all():
    hospital_name =  request.args.get('hospital_name')
    db = base.globalDB()
    db.connecter()
    result = db.select_robot_count_all(hospital_name)
    print(result)
    # JSON 형식으로 결과 반환
    return jsonify({
        'total_count': result['total_count'],
        'operating_count': result['operating_count'],
        'broken_count': result['broken_count'],
        'repair_count': result['repair_count']
    })
    
@app.route('/get_hospital_name', methods=['GET'])
def get_hospital_name():
    hospital_id = request.args.get('hospital_name')
    db = base.globalDB()
    db.connecter()
    
    # hospital_id로 병원 이름을 조회하는 쿼리
    query = "SELECT hospital_name FROM hospital_tb WHERE hospital_id = %s"
    db.cursors.execute(query, (hospital_id,))
    result = db.cursors.fetchone()

    if result:
        return jsonify({'hospital_name': result[0]})  # 병원 이름을 반환
    return jsonify({'hospital_name': 'Unknown'})  # 결과가 없을 경우

@app.route('/get_robo_regist_all_data', methods=['GET'])
def get_robo_all_data():
    hospital_name = request.args.get('hospital_name')
    db = base.globalDB()
    db.connecter() 
    result = db.select_robot_regist_all(hospital_name)
    # print(result)
    # JSON 형식으로 결과 반환
    return jsonify(result)

@app.route('/get_total_alert_data', methods=['GET'])
def get_total_alert_data():
    hospital_name = request.args.get('hospital_name')
    db = base.globalDB()
    db.connecter()
    
    result = json.loads(db.get_alarm_data(hospital_name))

    for item in result:
        robot_info = db.get_robot_info(item['robot_id'])
        if robot_info:
            ward = robot_info['ward']
            room = robot_info['room']
            item['place'] = f"{ward} {room}"  # '2병동 201호' 형식으로 설정
        else:
            item['place'] = "복도"  # 정보가 없을 경우 '정보 없음'으로 설정

    # JSON 형식으로 결과 반환
    return jsonify(result)

@app.route('/get_image_url')
def get_image_url():
    hospital_name = request.args.get('hospital_name')
    floor = request.args.get('floor')
    db = base.globalDB()
    db.connecter()
     # DB에서 이미지 URL 가져오기
    image_url = db.get_image_url(hospital_name, floor)

    if image_url:
        return jsonify({'url': image_url})  # URL을 JSON 형태로 반환
    return jsonify({'error': 'Image not found'}), 404  # 이미지가 없으면 404 반환

@app.route('/get_images', methods=['GET'])
def get_images():
    hospital_name = request.args.get('hospital_name')
    db = base.globalDB()
    db.connecter()
    
    image_data = db.get_images(hospital_name)  # url과 floor 필드를 함께 가져오기
    return jsonify({'images': image_data})

@app.route('/signin', methods=['POST'])
def signin():
    values = request.get_json()
    db = base.globalDB()
    db.connecter()
    result = db.signin(values)
    print(result)
    return result

@app.route('/static/<path:filename>')
def serve_static_file(filename):
    try:
        # static 폴더에서 파일을 반환
        return send_from_directory('static', filename)
    except FileNotFoundError:
        abort(404)  # 파일이 없으면 404 에러 반환

@app.route('/input_action', methods=['POST'])
def input_action():
    data = request.get_json()
    name = data.get('name')
    comment = data.get('comment')
    num = data.get('id')
    time = data.get('action_time')
    print(time)

    db = base.globalDB()
    db.connecter()
    db.insertAction(name, comment, num, time)

    return jsonify({"message": "Data saved successfully"})


##########################################################
##########################################################

if __name__ == "__main__":
    db = base.globalDB()
    db.connecter()
    client = start_mqtt_client()  # MQTT 클라이언트 시작

    socketio.run(app, host='0.0.0.0', port=8080)