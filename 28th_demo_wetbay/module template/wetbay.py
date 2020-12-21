#!/usr/bin/env python
from flask import Flask, request, jsonify
from time import sleep
app = Flask(__name__)

tray_presense = [0,0,0,0,0,0] # this should be get from sensor
error_slot = []

def checktray():
    global tray_presense
    # check sensor reading and append the tray_presense variable
    #
    #
    return tray_presense

def extend_tray(tray_number):
    print('Extending tray number: ' + str(tray_number))
    # put actual swtich on gas cylinder relay here, turn it blower and swipe a few times if necessary, turn off blower after fully extended
    #
    #
    # sleep(3)
    print("Tray extended")
    return "1"

def retract_tray(tray_number):
    print('Retracting tray number: ' + str(tray_number))
    # put actual swtich on gas cylinder relay here, turn it off after receive command
    #
    #
    # sleep(3)
    print("Tray retracted")
    return "Tray retracted"

def error_tray(tray_number):
    global error_slot
    error_slot.append(tray_number) # update global vairable about problematic tray
    print('Tray number: ' + str(tray_number) + ' has encountered problem')
    # put code to change led to tray_number to red
    #
    #
    #
    print("Please resolve...")
    return 'Error raised'

def error_resolved():
    global error_slot
    for x in error_slot:
        print("Problematic tray " + str(x) + " has been resolved, extending...")
        # change led back to green
        # 
        #
    error_slot = [] # clear global variable
    return "Acknowledged"

@app.route('/updatestatus', methods = ['POST'])
def updatestatus():
    global tray_presense
    data = request.get_json()
    pigeonhole = int(data['pigeonhole'])
    value = int(data['value'])
    print(pigeonhole, value)
    tray_presense[pigeonhole-1] = value
    print(tray_presense)
    return 'update successful'
    


# Main communication route from system pc to wetbay controller
@app.route('/action', methods = ['POST'])
def action():
    data = request.get_json()
    task = data['task']
    if task == "tray_presense":
        return jsonify({'tray_presense':checktray()})
    elif task == "extend_tray":
        return extend_tray(data['value'])
    elif task == "retract_tray":
        return retract_tray(data['value'])
    elif task == "error_tray":
        return error_tray(data['value'])
    elif task == "error_resolved":
        return error_resolved()


if __name__ == "__main__":  
    app.run(host='0.0.0.0', debug=True, port=5003)
    