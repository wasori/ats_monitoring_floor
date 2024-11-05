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

###########################################################
###########################################################

@app.route('/')
def index():
    return render_template('index.html')  # main.html 렌더링

@app.route('/main')
def main():
    return render_template('robo.html')  # main.html 렌더링

###########################################################
###########################################################

# 메시지 수신 핸들러
def on_message(client, userdata, message):
    global db
    global sensor

    if message.topic == "ros_thermocam":
        db = base.globalDB()
        db.connecter()
        result = db.insert_temp(message.payload)

# MQTT 연결 설정
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("signin")

def start_mqtt_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message 

    client.connect("1.220.178.46", 11883, 60)
    
    # MQTT 루프를 비동기로 시작
    client.loop_start()

    return client

###########################################################
###########################################################

@app.route('/signin', methods=['POST'])
def signin():
    values = request.get_json()
    print(values)
    db = base.globalDB()
    db.connecter()
    result = db.signin(values)
    print(result)
    return result

##########################################################
##########################################################

if __name__ == "__main__":
    db = base.globalDB()
    db.connecter()
    client = start_mqtt_client()  # MQTT 클라이언트 시작

    socketio.run(app, host='0.0.0.0', port=8081)