#!/usr/bin/env python
from flask import Flask, request, jsonify
from time import sleep
app = Flask(__name__)

RingInstrumentDict = {"ForcepArteryAdson":1, "ForcepArteryCrile": 2, "HolderNeedleMayoHegar": 3, "HolderNeedleCrilewood": 4, "ForcepTissueLittlewood": 5, "ForcepTissueStilles": 6, "ForcepTissueBabcock": 7, "ScissorDressingNurses": 8, "ScissorMayo": 1, "ScissorDissectingMetzenbaum": 2, "ForcepSpongeHoldingRampley": 3}
    
@app.route('/get_status', methods = ['POST'])
def get_status():
    global RingInstrumentDict
    data = request.get_json()
    task = data['task']
    if task == "inst_count":
        return jsonify(RingInstrumentDict)
    elif task =="consumables":
        enough = True
        for x in RingInstrumentDict:
            if RingInstrumentDict[x] < 6:
                enough = False
                return '0'
        return '1'
    elif task == "retrieve":
        x = data['value']
        RingInstrumentDict[x] -= 1
        return 'successfully update'
    elif task == "refill":
        print("refilling")
        for x in data['value']:
            temp_dict = {x: data['value'][x] + RingInstrumentDict[x]}
            RingInstrumentDict.update(temp_dict)
        return 'Successfully refilled' 

if __name__ == "__main__":  
    app.run(debug=True, port=5006)
    
