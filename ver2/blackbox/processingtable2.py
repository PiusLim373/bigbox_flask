#!/usr/bin/env python
from flask import Flask, request, jsonify
from time import sleep
app = Flask(__name__)

#this flask shouldnt be this simple, have vision and record which bracket process is done etc
#or maybe this module can be combines with the ring inspection bay

TempBracket = True #if bracket exists
PositionerOpen = True #bracket positioner status, true=open, false = close

def ClosePositioner():
    #insert servo controlling code here
    pass

def OpenPositioner():
    #insert servo controlling code here
    pass

@app.route('/get_status', methods = ['POST'])
def get_status():
    global TempBracket, PositionerOpen
    data = request.get_json()
    task = data['task']
    if task == "consumables_check":
        if (TempBracket):
            return '1'
        else:
            return '0'

    elif task == "reload":
        #trigger UR process to trasnfer temp brac from wetbay pigeonhole#1 to processing table 2
        #subprocess.call('python ~/all_ws/goldfinger_ws/src/bigbox_flask/ver2/ros_msg_publisher/Recheck_publisher.py', shell = True)
        #
        TempBracket = True
        return 'successfully reloaded'

    elif task =="activate_maintask":
        #insert code to do open/close bracekt positioner here
        #
        #
        if PositionerOpen:
            ClosePositioner()
            PositionerOpen = False
        else: 
            OpenPositioner()
            PositionerOpen = True
        return 'Main task completed successfully'

if __name__ == "__main__":  
    app.run(debug=True, port=5013)
    
