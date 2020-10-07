#!/usr/bin/env python
from flask import Flask, request, jsonify
from time import sleep
app = Flask(__name__)

NonRingInstrumentDict = {"TowelClipJones":1, "ForcepDissectingGillies": 2, "ForcepDissectingMcindoe": 8, "HandleBardParker": 8, "RulerGraduatedMultipurpose": 8, "SpearRedivac": 8}
    
@app.route('/get_status', methods = ['POST'])
def get_status():
    global NonRingInstrumentDict
    data = request.get_json()
    task = data['task']
    if task == "inst_count":
        return jsonify(NonRingInstrumentDict)
    elif task =="consumables":
        enough = True
        for x in NonRingInstrumentDict:
            if NonRingInstrumentDict[x] < 6:
                enough = False
                return '0'
        return '1'
    elif task == "retrieve":
        x = data['value']
        NonRingInstrumentDict[x] -= 1
        return 'successfully update'
    elif task == "refill":
        print("refilling")
        for x in data['value']:
            temp_dict = {x: data['value'][x] + NonRingInstrumentDict[x]}
            NonRingInstrumentDict.update(temp_dict)
        return 'Successfully refilled' 


if __name__ == "__main__":  
    app.run(debug=True, port=5007)
    
