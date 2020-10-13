#!/usr/bin/env python
from flask import Flask, request, render_template, Response, json, jsonify, session, redirect, url_for, g
import requests
from time import sleep
import subprocess
import datetime
import rospy
from std_msgs.msg import String
app = Flask(__name__)
app.secret_key = "dummysecretkey"

LastMaintenanceTime = datetime.datetime.now()
LastRefillTime = datetime.datetime.now()

# flask url for all modules
WetBayFlask = "http://127.0.0.1:5002/get_status"
DryBayFlask = "http://127.0.0.1:5003/get_status"
MagilsBayFlask = "http://127.0.0.1:5004/get_status"
ConsumablesFlask = "http://127.0.0.1:5005/get_status"

RingSpareBayFlask = "http://127.0.0.1:5006/get_status"
NonRingSpareBayFlask = "http://127.0.0.1:5007/get_status"
TrayPaperBayFlask = "http://127.0.0.1:5008/get_status"
WrappingBayFlask = "http://127.0.0.1:5009/get_status"
PrinterBayFlask = "http://127.0.0.1:5010/get_status"
IndicatorDispenserFlask = "http://127.0.0.1:5011/get_status"
StickerTagPrinterFlask = "http://127.0.0.1:5012/get_status"
ProcessingTable2Flask = "http://127.0.0.1:5013/get_status"

web_status_text = "Greetings, welcome to Bigbox! To continue, load in necessary items as instructed and follow the steps below. Starts by pressing the 'Check Consumables' button."
web_stage = 0
pigeonhole_to_process = []
pigeonhole_processing = -1
consumables_error_list = []
consumables_SMACHRun = False
drywetmagil_error = False

def updateUI(message):
    global web_status_text
    web_status_text = message
    return True

def GrabConsumables():
    ConsumablesDict = {}
    ModulesList = ["RingSpareBay", "NonRingSpareBay", "TempBracket", "TrayPaperBay", "WrappingBayPaper", "WrappingBayTape", "PrinterBayWrapper", "PrinterBayA4Paper", "IndicatorDispenser", "StickerTagPrinter"]
    # ModulesList = ["RingSpareBay", "NonRingSpareBay"]
    
    for x in ModulesList:
        task = {'task':'consumables_check'}
        if x == "TempBracket":
            ConsumablesDict.update({x:int(requests.post(ProcessingTable2Flask, json = task).content)})
        elif x == "WrappingBayPaper":
            task = {'task':'consumables_check_paper'}
            ConsumablesDict.update({x:int(requests.post(WrappingBayFlask, json = task).content)})
        elif x == "WrappingBayTape":
            task = {'task':'consumables_check_tape'}
            ConsumablesDict.update({x:int(requests.post(WrappingBayFlask, json = task).content)})
        elif x == "PrinterBayWrapper":
            task = {'task':'consumables_check_wrapper'}
            ConsumablesDict.update({x:int(requests.post(PrinterBayFlask, json = task).content)})
        elif x == "PrinterBayA4Paper":
            task = {'task':'consumables_check_a4paper'}
            ConsumablesDict.update({x:int(requests.post(PrinterBayFlask, json = task).content)})
        else:
            ConsumablesDict.update({x:int(requests.post(eval(x + "Flask"), json = task).content)})
    print(ConsumablesDict)
    return ConsumablesDict

@app.route('/statusSSE')
def statusSSE():
    
    def gen1():
        status_text_temp = ""
        web_stage_temp = 1
        pigeonhole_processing_temp = 0
        while True:
            if status_text_temp != web_status_text or web_stage_temp != web_stage or pigeonhole_processing_temp != pigeonhole_processing:
                print("SSE triggerred")
                print(pigeonhole_processing)
                previous_status_text = status_text_temp
                status_text_temp = web_status_text
                web_stage_temp = web_stage
                pigeonhole_processing_temp = pigeonhole_processing
                # print('data:{"web_status_text":"' + str(web_status_text) + '", "web_stage": "' + str(web_stage) + '"}\n\n')
                yield 'data:{"web_status_text":"' + str(web_status_text) + '", "web_previous_status_text" : "' + previous_status_text +'" ,"web_stage": ' + str(web_stage) + ', "pigeonhole_processing": ' + str(pigeonhole_processing) +'}\n\n'
    return Response(gen1(), mimetype='text/event-stream')

@app.route('/CheckConsumables', methods = ['GET', 'POST'])
def CheckConsumables():
    global consumables_error_list, consumables_SMACHRun
    ConsumablesDict = GrabConsumables()
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
        success = 0
        if len(consumables_error_list) == 0:
            success = 1
            
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

@app.route('/RefillConsumables', methods = ['POST'])
def RefillConsumables():
    data = request.get_json()
    if (data['module'] == "NonRingSpareBay") or (data['module'] == "RingSpareBay"):
        if data['action'] == "inst_count":
            task = {'task':'inst_count'}
            return json.loads(requests.post(eval(data['module'] + "Flask"), json = task).content)
        elif data['action'] == "refill":
            task = {'task':'refill', 'value':data['value']}
            requests.post(eval(data['module'] + "Flask"), json = task)
            return 'True'
    elif (data['module'] == "TempBrac"):
        if data['action'] == "reload":
            task = {'task':'reload'}
            return str(requests.post(ProcessingTable2Flask, json = task).content)
        elif data['action'] == "consumables_check":
            task = {'task':'consumables_check'}
            sleep(5)
            print("returning")
            requests.post(ProcessingTable2Flask, json = task)
            return 'True'
    elif(data['module'] == "WrappingBayPaper" or data['module'] == "WrappingBayTape"):
        if data['action'] == "reload_paper":
            task = {'task':'reload_paper'}
        elif data['action'] == "reload_tape":
            task = {'task':'reload_tape'}
        requests.post(WrappingBayFlask, json = task)
        return 'True'
    
    elif(data['module'] == "PrinterBayWrapper" or data['module'] == "PrinterBayA4Paper"):
        if data['action'] == "reload_wrapper":
            task = {'task':'reload_wrapper'}
        elif data['action'] == "reload_a4paper":
            task = {'task':'reload_a4paper'}
        requests.post(PrinterBayFlask, json = task)
        return 'True'

    elif(data['module'] == "TrayPaperBay" or data['module'] == "IndicatorDispenser" or data['module'] == "StickerTagPrinter"):
        task = {'task': data['action']}
        requests.post(eval(data['module'] + "Flask"), json = task)
        return 'True'

@app.route('/control_panel', methods = ['GET'])
def control_panel():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('control_panel.html')



@app.route('/CheckConsumablesLoaded', methods = ['GET'])
def CheckConsumablesLoaded():
    # trigger smach here
    print("process started")
    subprocess.call('python ~/all_ws/goldfinger_ws/src/bigbox_flask/ver2/ros_msg_publisher/ErrorResolve_or_NextStage_publisher.py', shell = True)
    return '1'

@app.route('/CheckDryWetMagil', methods = ['GET'])
def CheckWetDryBay():
    # trigger smach here
    print("process started")
    subprocess.call('python ~/all_ws/goldfinger_ws/src/bigbox_flask/ver2/ros_msg_publisher/Recheck_publisher.py', shell = True)
    return '1'

@app.route('/StartProcess', methods = ['GET'])
def StartProcess():
    # trigger smach here
    print("process started")
    subprocess.call('python ~/all_ws/goldfinger_ws/src/bigbox_flask/ver2/ros_msg_publisher/ErrorResolve_or_NextStage_publisher.py', shell = True)
    return '1'

        

@app.route('/SMACHPing', methods = ['POST']) #use to transfer message from smach to webUI
def SMACHPing():
    global web_stage, pigeonhole_processing
    data = request.get_json()
    if data['task'] == "next_stage":
        web_stage += 1
    if data['task'] == "updateUI":
        updateUI(data['input'])
    if data['task'] == "chg_web_stage":
        web_stage = data['input']
    if data['task'] == "pigeonhole_processing":
        pigeonhole_processing = data['input']
    return '1'

###################### For Page Routing


@app.route('/index', methods = ['GET'])
def index():
    if (not g.user) or (g.user.username != "admin"):
        return redirect(url_for('login')) 
    return render_template('index.html')

@app.route('/refill', methods = ['GET'])
def refill():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('refill.html')

@app.route('/spawn_modal', methods = ['GET'])
def spawn_modal():
    return render_template('modal.html')

@app.route('/MaintenanceTime', methods = ['GET', 'POST'])
def MaintenanceTime():
    global LastMaintenanceTime, LastRefillTime
    if request.method == 'GET':
        timestamp_maintenance = (LastMaintenanceTime - datetime.datetime(1970, 1, 1)).total_seconds()
        timestamp_refill = (LastRefillTime - datetime.datetime(1970, 1, 1)).total_seconds()
        
        returndict = {'timestamp_refill':timestamp_refill, 'timestamp_maintenance': timestamp_maintenance}
        return jsonify(returndict)

###################### For User logging

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

users = []
users.append(User(id = 1, username = "admin", password = "bigboxadmin"))
users.append(User(id = 2, username = "operator", password = "operator"))

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user
        

@app.route('/', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)
        username = request.form['username']
        password = request.form['password']
        try:
            user = [x for x in users if x.username == username][0]
            if user and user.password == password:
                session['user_id'] = user.id
                if username == "admin":
                    return redirect(url_for('index')) 
                elif username == "operator":
                    return redirect(url_for('control_panel'))
                else:
                    print(error)
                    return redirect(url_for('login'))
        except:
            return redirect(url_for('login')) 
        return redirect(url_for('login'))
    else:    
        return render_template('login.html')

@app.route('/logout', methods = ['GET'])
def logout():
    try:
        session.pop('user_id', None)
        g.user = None
        print("logged out")
        return redirect(url_for('login'))
    except:
        pass

if __name__ == "__main__":
    app.run(debug=True, port=5001)