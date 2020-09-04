#!/usr/bin/env python
from time import sleep
from flask import Flask, request, render_template
app = Flask(__name__)

wetbay_database = {'tray_presense':[0,0,0,0,0,0], 'extend_tray':0, 'error_tray':0}

def extend_tray(tray_number):
    print("extending tray number: " + str(tray_number))
    sleep(3)
    print("Extension completed")
    return True

@app.route('/variable_update', methods = ['GET','POST'])
def variable_update():
    global wetbay_database
    if request.method == 'GET':
        return wetbay_database
    else:
        data = request.get_json()
        wetbay_database = data
        return 'Update successful'

@app.route('/extend_tray', methods = ['POST'])
def extend_tray_flaskcall():
    global wetbay_database
    data = request.get_json()
    #data sample: {'extend_tray' : 1}
    #extend of tray of number x here
    wetbay_database['extend_tray'] = data['extend_tray']
    extend_tray()
    
    

if __name__ == "__main__":
    app.run(debug=True)