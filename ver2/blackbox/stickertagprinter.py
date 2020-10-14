#!/usr/bin/env python
from flask import Flask, request, jsonify
from time import sleep
app = Flask(__name__)

StickerTag = 3 #sticker tag loaded in the machine

@app.route('/get_status', methods = ['POST'])
def get_status():
    global StickerTag
    data = request.get_json()
    task = data['task']
    if task == "consumables_check":
        if StickerTag < 5:
            return '0'
        else:
            return '1'
    elif task == "consumables_count":
        return str(StickerTag)
    elif task == "reload":
        StickerTag = 100
        return 'successfully reloaded'
    elif task =="activate_maintask":
        #insert code to do print tag, number of sticker tag will be reduced
        #
        #
        StickerTag -= 1
        return 'Main task completed successfully'

if __name__ == "__main__":  
    app.run(debug=True, port=5012)
    
