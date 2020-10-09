#!/usr/bin/env python
from flask import Flask, request, jsonify
from time import sleep
app = Flask(__name__)

WrappingPaper = 200 #paper per stack of crepe loaded, to estimate number of paper left
A4Paper = 500 #a4 paper per pack

@app.route('/get_status', methods = ['POST'])
def get_status():
    global WrappingPaper, A4Paper
    data = request.get_json()
    task = data['task']
    if task == "consumables_check_wrapper":
        if WrappingPaper < 10:
            return '0'
        else:
            return '1'
    elif task == "consumables_check_a4paper":
        if A4Paper < 25:
            return '0'
        else:
            return '1'
    elif task == "reload_wrapper":
        WrappingPaper = 200
        return 'successfully reloaded'
    elif task == "reload_a4paper":
        A4Paper = 500
        return 'successfully reloaded'
    elif task =="activate_maintask":
        #insert code to do print logsheet, dispense paper and perform folding here, number of a4paper and wrapper will be reduced
        #
        #
        WrappingPaper -= 1
        A4Paper -= 2 #should be printing 2 pieces
        return 'Main task completed successfully'

if __name__ == "__main__":  
    app.run(debug=True, port=5010)
    
