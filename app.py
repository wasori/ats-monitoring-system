# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template, url_for, g, request, send_from_directory, abort
from flask_socketio import SocketIO
from datetime import datetime, timedelta
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
        message_payload = message.payload.decode('utf-8') 

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
        
        print(jsonmsg)

        db = base.globalDB()
        db.connecter()

        visionjson = db.select_vision_uptime()
        vision = json.loads(visionjson)
        print(vision)

        db.insert_vision(message.payload)

        falldown = str(jsonmsg["falldown"])
        
        print( falldown )
        pose_value  = str(jsonmsg["pose"])
        hos_name = str(jsonmsg["hospital_name"])
        roonbed = jsonmsg['patient_no'].split('-')

        

        pose = 0
        down = 0
        check = -1

        for i in range(0, len(vision)):
            if vision[i]['room'] == int(roonbed[0]) and vision[i]['sickbed'] == int(roonbed[1]):
                check = i
                break
            
        if jsonmsg["falldown"]:
            content = "down"
            value = "1"

            insertdata = (
                '{"rid":"'+jsonmsg["robot_id"]+'", "xaxis":"'+str(int(roonbed[0]))+ 
                '", "yaxis":"'+str(int(roonbed[1]))+'", "content":"'+content+ 
                '", "value":"'+value+'", "hos_name" : "'+hos_name+'"}'
            )

            print("Insert Data:", insertdata) 
            db.insert_alarm(insertdata) 
        else:
            if check != -1:
                if vision[check]['pose'] == pose_value:
                    pose = 1
                elif vision[check]['pose'] == "none":
                    pose = 0
            else:
                pose = 0

            if pose == 1 :
                content = "pose" 
                value = pose_value

                insertdata = (
                    '{"rid":"'+jsonmsg["robot_id"]+'", "xaxis":"'+str(int(roonbed[0]))+
                    '", "yaxis":"'+str(int(roonbed[1]))+'", "content":"'+content+
                    '", "value":"'+value+'", "hos_name" : "'+hos_name+'"}'
                )

                print("Insert Data:", insertdata) 
                db.insert_alarm(insertdata)


    elif message.topic == "robot_position":
        message_payload = message.payload.decode('utf-8') 
        jsonmsg = json.loads(message.payload)

        db = base.globalDB()
        db.connecter()
        db.insert_robot(message.payload)
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
    
    client.loop_start()

    return client

####################################################################
####################################################################

# Flask 라우팅
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main')
def main():
    return render_template('main.html') 

@app.route('/test')
def test():
    return render_template('test.html') 

####################################################################
####################################################################

@app.route('/send_pose_data', methods=['POST'])
def send_pose_data():
    data = request.get_json()
    print("Received pose data:", data)
    
    client.publish("aos_pose_detect_result", json.dumps(data))
    
    return jsonify({"message": "Pose data sent!"})

@app.route('/send_sensor_data', methods=['POST'])
def send_sensor_data():
    data = request.get_json() 
    print("Received sensor data:", data)
    
    client.publish("sensor", json.dumps(data))
    
    return jsonify({"message": "Sensor data sent!"})

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
    
    query = "SELECT hospital_name FROM hospital_tb WHERE hospital_id = %s"
    db.cursors.execute(query, (hospital_id,))
    result = db.cursors.fetchone()

    if result:
        return jsonify({'hospital_name': result[0]}) 
    return jsonify({'hospital_name': 'Unknown'}) 

@app.route('/get_robo_regist_all_data', methods=['GET'])
def get_robo_all_data():
    hospital_name = request.args.get('hospital_name')
    db = base.globalDB()
    db.connecter() 
    result = db.select_robot_regist_all(hospital_name)
    return jsonify(result)

@app.route('/get_total_alert_data', methods=['GET'])
def get_total_alert_data():
    hospital_name = request.args.get('hospital_name')
    db = base.globalDB()
    db.connecter()
    
    result = json.loads(db.get_alarm_data(hospital_name))

    for item in result:
        robot_info = db.get_robot_info(item['robot_id'])
        if item["content"] in ["down", "pose"]:
            item['place'] = f"{item['x']}호 {item['y']}병상"
        else:
            if robot_info:
                ward = robot_info['ward']
                room = robot_info['room']
                item['place'] = f"{ward} {room}"
            else:
                item['place'] = "복도"

    return jsonify(result)

@app.route('/get_image_url')
def get_image_url():
    hospital_name = request.args.get('hospital_name')
    floor = request.args.get('floor')
    db = base.globalDB()
    db.connecter()
    image_url = db.get_image_url(hospital_name, floor)

    if image_url:
        return jsonify({'url': image_url}) 
    return jsonify({'error': 'Image not found'}), 404

@app.route('/get_images', methods=['GET'])
def get_images():
    hospital_name = request.args.get('hospital_name')
    db = base.globalDB()
    db.connecter()
    
    image_data = db.get_images(hospital_name)
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
        return send_from_directory('static', filename)
    except FileNotFoundError:
        abort(404)

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

@app.route('/get_robo_regist', methods=['GET'])
def get_robo_regist():
    hospital = request.args.get('hospital_name')
    db = base.globalDB()
    db.connecter()
    result = db.get_robo_regist(hospital)

    return jsonify(result)

@app.route('/register_robo', methods=['POST'])
def register_robo():
    data = request.get_json()

    robot_id = data.get('robot_id')
    hospital_name = data.get('hospital_name')
    ward = data.get('ward')
    room = data.get('room')
    state = data.get('state')
    hospital_id = data.get('hospital_id')

    db = base.globalDB()
    db.connecter()

    query = f"""
        INSERT INTO robot_regist_tb (robot_id, hospital_name, ward, room, state, regist_date, hospital_id)
        VALUES ('{robot_id}', '{hospital_name}', '{ward}', '{room}', '{state}', CURRENT_TIMESTAMP, '{hospital_id}')
    """

    if db.cursors == "":
        return jsonify({"success": False, "message": "DB not connected"})
    
    try:
        db.cursors.execute(query)
        db.connection.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.connection.rollback()
        return jsonify({"success": False, "message": str(e)})

@app.route('/input_robo_regist', methods=['POST'])
def input_robo_regist():
    data = request.get_json()
    print(data)
    robot_id = data.get('robot_id')
    hospital_name = data.get('hospital_name')
    ward = data.get('ward')
    room = data.get('room')
    state = data.get('state')
    hospital_id = data.get('hospital_id')

    try:
        db = base.globalDB()
        db.connecter()
        db.insert_robot_regist(robot_id, hospital_name, ward, room, state, hospital_id)

        return jsonify({"message": "로봇이 성공적으로 등록되었습니다."})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400  # 중복 시 400 에러 반환
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "로봇 등록 중 오류 발생"}), 500
    
@app.route('/input_hospital_regist', methods=['POST'])
def input_hospital_regist():
    try:
        data = request.get_json()
        hospital_name = data.get('hospital_name')
        ward = data.get('ward')
        room = data.get('room')
        ward_photo = data.get('ward_photo')
        hospital_id = data.get('hospital_id')

        db = base.globalDB()
        db.connecter()
        db.insert_hospital_regist(hospital_name, ward, room, ward_photo, hospital_id)

        return jsonify({"message": "병동이 성공적으로 등록되었습니다."}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400  # 유효성 검사 실패
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "병동 등록 중 오류 발생"}), 500
    
@app.route('/get_content_stats')
def get_content_stats():
    db = base.globalDB()
    db.connecter()

    try:
        query = """
            SELECT content, COUNT(*) as count
            FROM alarm_data_tb
            GROUP BY content
        """
        db.cursors.execute(query)
        data = db.cursors.fetchall()

        content_map = {
            'down': '낙상',
            'water': '물감지',
            'dust': '먼지감지',
            'fire': '화재감지',
            'pose': '욕창감지'
        }

        result = [
            {'content': content_map.get(row[0], row[0]), 'count': row[1]}
            for row in data
        ]

    except Exception as e:
        print(f"Error: {e}")
        result = {'error': '데이터를 가져오는 중 문제가 발생했습니다.'}

    finally:
        db.cursors.close()

    return jsonify(result)

@app.route('/get_content_stats_by_date')
def get_content_stats_by_date():
    content = request.args.get('content', None)

    if not content:
        return jsonify({'error': 'content 파라미터가 필요합니다.'})

    db = base.globalDB()
    db.connecter()

    try:
        query = """
            SELECT DATE_FORMAT(uptime, '%%Y-%%m-%%d') as date, COUNT(*) as count
            FROM alarm_data_tb
            WHERE content = %s
            GROUP BY date
            ORDER BY date
        """
        db.cursors.execute(query, (content,))
        data = db.cursors.fetchall()

        db_results = {row[0]: row[1] for row in data}

        if db_results:
            start_date = datetime.strptime(min(db_results.keys()), "%Y-%m-%d")
            end_date = datetime.strptime(max(db_results.keys()), "%Y-%m-%d")
        else:
            start_date = datetime.now()
            end_date = datetime.now()

        date_range = []
        current_date = start_date
        while current_date <= end_date:
            date_range.append(current_date.strftime("%Y-%m-%d"))
            current_date += timedelta(days=1)

        result = [
            {'date': date, 'count': db_results.get(date, 0)}
            for date in date_range
        ]

        return jsonify(result)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': '데이터를 가져오는 중 문제가 발생했습니다.'})
    finally:
        db.cursors.close()

##########################################################
##########################################################

if __name__ == "__main__":
    db = base.globalDB()
    db.connecter()
    client = start_mqtt_client()

    socketio.run(app, host='0.0.0.0', port=8080)