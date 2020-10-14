#!/usr/bin/env python
from flask import Flask, request, jsonify
from time import sleep
app = Flask(__name__)

WrappingPaper = 200 #paper per stack of crepe loaded, to estimate number of paper left
MaskingTape = 2 #tape per roll, estimated to seal 100 wrapped packages

@app.route('/get_status', methods = ['POST'])
def get_status():
    global WrappingPaper, MaskingTape
    data = request.get_json()
    task = data['task']
    if task == "consumables_check_paper":
        if WrappingPaper < 10:
            return '0'
        else:
            return '1'
    elif task == "consumables_check_tape":
        if MaskingTape < 5:
            return '0'
        else:
            return '1'
    elif task == "consumables_count_paper":
        return str(WrappingPaper/2)
    elif task == "consumables_count_tape":
        return str(MaskingTape/2)
    elif task == "reload_paper":
        WrappingPaper = 200
        return 'successfully reloaded'
    elif task == "reload_tape":
        MaskingTape = 100
        return 'successfully reloaded'
    elif task =="activate_maintask":
        #insert code to do the folding here, reduce the wrapping paper and tape count by 1
        #
        #
        WrappingPaper -= 1
        MaskingTape -= 1
        return 'Main task completed successfully'

if __name__ == "__main__":  
    app.run(debug=True, port=5009)
    
