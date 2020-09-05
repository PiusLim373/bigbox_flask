#!/usr/bin/env python
from flask import Flask, request, render_template, Response, json, jsonify
import requests
from time import sleep
import subprocess
import datetime
import rospy
from std_msgs.msg import String
app = Flask(__name__)

LastMaintenanceTime = datetime.datetime.now()

# flask url for all modules
WetBayFlask = "http://127.0.0.1:5002/get_status"
DryBayFlask = "http://127.0.0.1:5003/get_status"
MagilsBayFlask = "http://127.0.0.1:5004/get_status"
ConsumablesFlask = "http://127.0.0.1:5005/get_status"



web_status_text = "Greetings, welcome to Bigbox! To continue, load in necessary items as instructed and follow the steps below. Starts by pressing the 'Check Consumables' button."
web_stage = 0
pigeonhole_to_process = []
consumables_error_list = []
consumables_SMACHRun = False
drywetmagil_error = False

def updateUI(message):
    global web_status_text
    web_status_text = message
    return True

@app.route('/statusSSE')
def statusSSE():
    
    def gen1():
        status_text_temp = ""
        web_stage_temp = 1
        while True:
            if status_text_temp != web_status_text or web_stage_temp != web_stage:
                print("SSE triggerred")
                previous_status_text = status_text_temp
                status_text_temp = web_status_text
                web_stage_temp = web_stage
                # print('data:{"web_status_text":"' + str(web_status_text) + '", "web_stage": "' + str(web_stage) + '"}\n\n')
                yield 'data:{"web_status_text":"' + str(web_status_text) + '", "web_previous_status_text" : "' + previous_status_text +'" ,"web_stage": ' + str(web_stage) + '}\n\n'
    return Response(gen1(), mimetype='text/event-stream')

@app.route('/CheckConsumables', methods = ['GET', 'POST'])
def CheckConsumables():
    global consumables_error_list, consumables_SMACHRun
    # collect all consumables data from diff modules, using hardcoded variables as of now
        # eg:
        #   for x in ConsumablesDict:
        #       data = requests.post(x + URL + /get_consumable , json = data)
        #       ConsumablesDict[x] = int(data.text)
        #
    task = {'task': 'consumables_presense'}
    ConsumablesDict = json.loads(requests.post(ConsumablesFlask, json = task).content)
    if request.method == 'GET': #for smach access
        print("SMACHRun chg to true")
        consumables_SMACHRun = True
        updateUI("Checking consumables....") #update GUI current status
        sleep(1)
        consumables_error_list = []
        for x in ConsumablesDict:
            print("checking consumables for module: " + str(x))
            if not ConsumablesDict[x]:
                consumables_error_list.append(x)
        if len(consumables_error_list) != 0:
            s = ""
            for x in consumables_error_list:
                s += x + ', '
            print("Consumables checking failed, error in following modules: " + s)
            updateUI("Consumables checking failed, please check the info below")
            sleep(1)
            return 'False' # return false to smach
        else:
            print("Consumables checking successful")
            updateUI("Consumables checking successful")
            sleep(1)
            return 'True' # return true to smach
    else: # for webui access
        success = 1
        if len(consumables_error_list) != 0:
            success = 0
        if not consumables_SMACHRun:
            success = 2
        response = {'check_success': success, 'ConsumablesDict': ConsumablesDict}
        return jsonify(response)
        # ConsumablesDict = {'RingSpareBay' : RingSpareBayCon, 'NonRingSpareBay' : NonRingSpareBayCon, 'TempBracket' : TempBracketCon, 'TrayPaper' : TrayPaperCon, 'WrappingPaper' : WrappingPaperCon, 'WrappingSealer' : WrappingSealerCon, 'PrintedListWrapper' : PrintedListWrapperCon, 'A4Paper' : A4PaperCon, 'IndicatorDispenser' : IndicatorDispenserCon, 'StickerTag' : StickerTagCon}
    

@app.route('/CheckWetDryMagil', methods = ['GET','POST']) # run by smach to obtain pigeonhole to process
def CheckTrayCoverContainer():
    global pigeonhole_to_process, drywetmagil_error
    task = {'task': 'tray_presense'}
    tray = json.loads(requests.post(WetBayFlask, json = task).content)
    task = {'task': 'cover_presense'}
    cover = json.loads(requests.post(DryBayFlask, json = task).content)
    task = {'task': 'container_presense'}
    container = json.loads(requests.post(DryBayFlask, json = task).content)
    task = {'task': 'cc_presense'}
    cc = json.loads(requests.post(DryBayFlask, json = task).content)
    task = {'task': 'magil_presense'}
    try:
        magil = len(json.loads(requests.post(MagilsBayFlask, json = task).content))
    except:
        magil = 0
    if request.method == 'GET': #from smach
        print("request get /CheckWetDryMagil run")
        updateUI("Checking Wetbay and Drybay for tray, cover and container....") #update GUI current status
        pigeonhole_to_process = []
        drywetmagil_error = False
        for i in range(6):
            # print()
            if tray[i] and cc[i]:
                pigeonhole_to_process.append(i)
            elif tray[i] and (not cc[i]):
                print("drybay slot "+str(i)+" not loaded" )
                drywetmagil_error = True
                updateUI("Loading error, please check below")
                error = {'task':'error_tray', 'input':i}
                requests.post(DryBayFlask, json = error)
            elif (not tray[i]) and cc[i]:
                print("wetbay slot "+str(i)+" not loaded" )
                drywetmagil_error = True
                updateUI("Loading error, please check below")
                error = {'task':'error_tray', 'input':i}
                requests.post(WetBayFlask, json = error)
        if(magil < len(pigeonhole_to_process)): # number of magil is less than pigeonhole to process
            drywetmagil_error = True
            updateUI("Number of Magil's Tube available is fewer than tray to be processed, please reload.")
            print("magil error")
        if len(pigeonhole_to_process) == 0 or drywetmagil_error:
            if len(pigeonhole_to_process) == 0:
                updateUI("No slot is loaded, please load in Tray, Cover and Container to continue")
            sleep(1)
            return 'False' # return false to smach
        else:
            updateUI("Checking successful, check below for pigeon hole to be processed. Press 'Start Process' to proceed.")
            sleep(1)
            print(pigeonhole_to_process)
            return str(pigeonhole_to_process) # return pigeonhole_to_process list count to smach
    else: # from webui
        print(pigeonhole_to_process)
        response = {'error': drywetmagil_error, 'tray':tray, 'cover':cover, 'container':container, 'cc':cc, 'pigeonhole_to_process': pigeonhole_to_process, 'magil':magil} 
        return jsonify(response)


@app.route('/control_panel', methods = ['GET'])
def control_panel():
    return render_template('control_panel.html')



@app.route('/CheckConsumablesLoaded', methods = ['GET'])
def CheckConsumablesLoaded():
    # trigger smach here
    print("process started")
    subprocess.call('python ~/all_ws/goldfinger_ws/src/bigbox_flask/ver2/publisher.py', shell = True)
    return '1'

@app.route('/CheckDryWetMagil', methods = ['GET'])
def CheckWetDryBay():
    # trigger smach here
    print("process started")
    subprocess.call('python ~/all_ws/goldfinger_ws/src/bigbox_flask/ver2/publisher.py', shell = True)
    return '1'

@app.route('/StartProcess', methods = ['GET'])
def StartProcess():
    # trigger smach here
    print("process started")
    subprocess.call('python ~/all_ws/goldfinger_ws/src/bigbox_flask/ver2/publisher.py', shell = True)
    return '1'

        

@app.route('/SMACHPing', methods = ['POST']) #use to transfer message from smach to webUI
def SMACHPing():
    global web_stage, web_resolve_btn
    data = request.get_json()
    if data['task'] == "next_stage":
        web_stage += 1
    if data['task'] == "spawn_resolve":
        web_resolve_btn = 1
    if data['task'] == "chg_web_stage":
        web_stage = data['input']
    return '1'

###################### For Index Page
@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

@app.route('/MaintenanceTime', methods = ['GET', 'POST'])
def MaintenanceTime():
    global LastMaintenanceTime
    if request.method == 'GET':
        timestamp = (LastMaintenanceTime - datetime.datetime(1970, 1, 1)).total_seconds()
        return str(timestamp)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
