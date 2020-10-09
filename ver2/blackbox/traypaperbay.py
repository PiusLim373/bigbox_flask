#!/usr/bin/env python
from flask import Flask, request, jsonify
from time import sleep
app = Flask(__name__)

TrayPaper = 200 #paper per stack of crepe loaded, to estimate number of paper left

@app.route('/get_status', methods = ['POST'])
def get_status():
    global TrayPaper
    data = request.get_json()
    task = data['task']
    if task == "consumables_check":
        if TrayPaper < 20:
            return '0'
        else: 
            return '1'
    elif task =="dispense_paper":
        #insert code to activate lifting mechanism to dispense 1 paper here
        TrayPaper -= 1
        return 'Dispensed'
    elif task == "reload":
        TrayPaper = 200
        return 'successfully reloaded'

if __name__ == "__main__":  
    app.run(debug=True, port=5008)
    
