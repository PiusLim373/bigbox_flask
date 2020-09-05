#!/usr/bin/env python
from flask import Flask, request
from time import sleep
app = Flask(__name__)

tray_presense = [1,1,1,1,0,1] # this should be get from sensor
error_slot = []

def checktray():
    global tray_presense
    # check sensor reading and append the tray_presense variable
    #
    #
    return str(tray_presense)

def extend_tray(tray_number):
    print('Extending tray number: ' + str(tray_number))
    # put actual swtich on gas cylinder relay here, turn it blower and swipe a few times if necessary, turn off blower after fully extended
    #
    #
    sleep(3)
    print("Tray extended")
    return "Tray extended"

def retract_tray(tray_number):
    print('Retracting tray number: ' + str(tray_number))
    # put actual swtich on gas cylinder relay here, turn it off after receive command
    #
    #
    sleep(3)
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

# Main communication route from system pc to wetbay controller
@app.route('/get_status', methods = ['POST'])
def get_status():
    data = request.get_json()
    task = data['task']
    if task == "tray_presense":
        return checktray()
    elif task == "extend_tray":
        return extend_tray(data['input'])
    elif task == "retract_tray":
        return retract_tray(data['input'])
    elif task == "error_tray":
        return error_tray(data['input'])
    elif task == "error_resolved":
        return error_resolved()


if __name__ == "__main__":  
    app.run(debug=True, port=5002)
    
