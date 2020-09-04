#!/usr/bin/env python
from flask import Flask, request
from time import sleep
app = Flask(__name__)

magil_presense = [1,1,1,1,1,1,1,1,1,1,1,1] # this should be get from sensor
#magil_presense = [0] * 12
current_position = 0 # the position where the end plate is covering the magil bay
error_slot = []

def checkmagil():
    global magil_presense
    # check sensor reading and append the magil_presense variable
    #
    #
    for x in magil_presense:
        if x != 0:
            return str(magil_presense)
    # prompt error if magils bay is empty during check
    return 'False'

def dispense_magil():
    global current_position
    print('Dispensing 1 magil from slot: ' + str(current_position))
    current_position += 1
    # put actual code to move slot to next postion
    #
    #
    sleep(2)
    print("Magil dispensed")
    return "Magil dispensed"

def refill_bay():
    global current_position
    print("Request to refilll bay, zeroing dispenser")
    # actual code to move the slot to position 0
    #
    #
    current_position = 0
    checkmagil()
    return "Refill completed"

# Main communication route from system pc to wetbay controller
@app.route('/get_status', methods = ['POST'])
def get_status():
    data = request.get_json()
    task = data['task']
    if task == "magil_presense":
        return checkmagil()
    elif task == "dispense_magil":
        return extend_tray()
    elif task == "refill_bay":
        return retract_tray()


if __name__ == "__main__":  
    app.run(debug=True, port=5004)
    
