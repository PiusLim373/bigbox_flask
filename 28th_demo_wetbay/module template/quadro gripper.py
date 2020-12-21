#!/usr/bin/env python
from flask import Flask, request
from time import sleep
app = Flask(__name__)

current_gripper = "parallel_gripper"

def change_gripper(gipper):
    global current_gripper
    if gripper == "parallel_gripper":
        # do necessary things here to the motor / servo to change to the gripper desired
        #
        #
        current_gripper = "parallel_gripper"    # udpate the current_gripper variable
        return 'True'   # return True if success, False is fail to change
    elif gripper == "suction_gripper":
        # do necessary things here to the motor / servo to change to the gripper desired
        #
        #
        current_gripper = "suction_gripper"     # udpate the current_gripper variable
        return 'True'   # return True if success, False is fail to change
    elif gripper == "tray_gripper":
        # do necessary things here to the motor / servo to change to the gripper desired
        #
        #
        current_gripper = "tray_gripper"        # udpate the current_gripper variable
        return 'True'   # return True if success, False is fail to change
    elif gripper == "tray_paper_gripper":
        # do necessary things here to the motor / servo to change to the gripper desired
        #
        #
        current_gripper = "tray_paper_gripper"  # udpate the current_gripper variable
        return 'True'   # return True if success, False is fail to change
    else: 
        print("invalid option")
        return 'False'

def gripper_action(action):
    if current_gripper == "parallel_gripper":
        if action == "grip":
            # do necessary things here to the motor / servo to perform the gripper action
            #
            #
            return 'True'   # return True if success, False is fail to change
        elif action == "release":
            # do necessary things here to the motor / servo to perform the gripper action
            #
            #
            return 'True'   # return True if success, False is fail to change
    elif current_gripper == "suction_gripper":
        if action == "grip":
            # do necessary things here to the motor / servo to perform the gripper action
            #
            #
            return 'True'   # return True if success, False is fail to change
        elif action == "release":
            # do necessary things here to the motor / servo to perform the gripper action
            #
            #
            return 'True'   # return True if success, False is fail to change
    elif current_gripper == "tray_gripper":
        if action == "grip":
            # do necessary things here to the motor / servo to perform the gripper action
            #
            #
            return 'True'   # return True if success, False is fail to change
        elif action == "release":
            # do necessary things here to the motor / servo to perform the gripper action
            #
            #
            return 'True'   # return True if success, False is fail to change
    elif current_gripper == "tray_paper_gripper":
        if action == "grip":
            # do necessary things here to the motor / servo to perform the gripper action
            #
            #
            return 'True'   # return True if success, False is fail to change
        elif action == "release":
            # do necessary things here to the motor / servo to perform the gripper action
            #
            #
            return 'True'   # return True if success, False is fail to change

# add more if needed
#
#

# Main communication route from system pc to wetbay controller
@app.route('/action', methods = ['POST'])
def action():
    data = request.get_json()
    task = data['task']
    if task == "change_gripper":
        return change_gripper(data['value'])
    elif task == "gripper_action":
        return gripper_action(data['value'])
    # add more if needed


if __name__ == "__main__":  
    app.run(host='0.0.0.0', debug=True, port=5003)
    