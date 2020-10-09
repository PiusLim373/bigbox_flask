#!/usr/bin/env python
from flask import Flask, request, jsonify
from time import sleep
app = Flask(__name__)

RingSpareBayCon = 0
NonRingSpareBayCon = 1 
TempBracketCon = 0
TrayPaperCon = 1
WrappingPaperCon = 1
WrappingSealerCon = 1
PrintedListWrapperCon = 1
A4PaperCon = 1
IndicatorDispenserCon = 1
StickerTagCon = 1

def compiledatabase():
    ConsumablesDict = {'RingSpareBay' : RingSpareBayCon, 'NonRingSpareBay' : NonRingSpareBayCon, 'TempBracket' : TempBracketCon, 'TrayPaper' : TrayPaperCon, 'WrappingPaper' : WrappingPaperCon, 'WrappingSealer' : WrappingSealerCon, 'PrintedListWrapper' : PrintedListWrapperCon, 'A4Paper' : A4PaperCon, 'IndicatorDispenser' : IndicatorDispenserCon, 'StickerTag' : StickerTagCon}
    return ConsumablesDict

@app.route('/get_status', methods = ['POST'])
def get_status():
    data = request.get_json()
    task = data['task']
    if task == "consumables_presense":
        return jsonify(compiledatabase())


if __name__ == "__main__":  
    app.run(debug=True, port=5005)
    
