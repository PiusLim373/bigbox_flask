#!/usr/bin/env python 
from flask import Flask, request, render_template, Response, json, jsonify
import requests
WetBayFlask = 'http://127.0.0.1:5003/action'

WetBayPigeonHoleExtended = [0,0,0,0,0,0]
WetBayPigeonHoleStatus = [0,0,0,0,0,0]
app = Flask(__name__)


def getpigeonholestatus():
    global WetBayPigeonHoleStatus
    action = {'task':'tray_presense'}
    temp = requests.post(WetBayFlask, json = action).text
    WetBayPigeonHoleStatus = json.loads(temp)['tray_presense']
    return True

@app.route('/pigholecontroller', methods = ['POST'])
def pigholecontroller():
    data = request.get_json()
    if WetBayPigeonHoleExtended[int(data['value']) - 1]:
        task = "retract_tray"
        WetBayPigeonHoleExtended[int(data['value'] - 1)] = 0
    else:
        task = "extend_tray"
        WetBayPigeonHoleExtended[int(data['value'] - 1)] = 1
    action = {'task':task, 'value':data['value']}
    print(action)
    requests.post(WetBayFlask, json = action)
    if task == "retract_tray":
        return "0"
    else:
        return "1"

@app.route('/get_status', methods = ['GET'])   
def get_status():
    return_str = ""
    getpigeonholestatus()
    for i in range(6):
        return_str += str(WetBayPigeonHoleStatus[i])
        if i != 5:
            return_str += ","
    # print(return_str)
    return return_str
    
@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5002)