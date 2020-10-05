#!/usr/bin/env python
from flask import Flask, request, jsonify
from time import sleep
app = Flask(__name__)

RingInstrumentDict = {"ForcepArteryAdson":8, "ForcepArteryCrile": 8, "HolderNeedleMayoHegar": 8, "HolderNeedleCrilewood": 8, "ForcepTissueLittlewood": 8, "ForcepTissueStilles": 8, "ForcepTissueBabcock": 8, "ScissorDressingNurses": 8, "ScissorMayo": 8, "ScissorDissectingMetzenbaum": 8, "ForcepSpongeHoldingRampley": 8}
    
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

@app.route('/refill', methods = ['POST'])
def refill():
    global RingInstrumentDict
    incomingdata = request.get_json()
    for x in incomingdata:
        temp_dict = {x: incomingdata[x] + RingInstrumentDict[x]}
        RingInstrumentDict.update(temp_dict)
    return 'successfully updated' 

if __name__ == "__main__":  
    app.run(debug=True, port=5006)
    
