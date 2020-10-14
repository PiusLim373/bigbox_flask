#!/usr/bin/env python
from flask import Flask, request, jsonify
from time import sleep
app = Flask(__name__)

Indicator = 1 #indicator loaded inside machine

@app.route('/get_status', methods = ['POST'])
def get_status():
    global Indicator
    data = request.get_json()
    task = data['task']
    if task == "consumables_check":
        if Indicator < 2:
            return '0'
        else: 
            return '1'
    elif task == "consumables_count":
        return str(Indicator)
    elif task == "reload":
        Indicator = 30
        return 'successfully reloaded'
    elif task =="activate_maintask":
        #insert code to do vibrate the mechanism and dispense 1 x indicator here, number of indicator will be reduced
        #
        #
        Indicator -= 1
        return 'Main task completed successfully'

if __name__ == "__main__":  
    app.run(debug=True, port=5011)
    
