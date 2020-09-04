#!/usr/bin/env python
from flask import Flask, request, render_template
app = Flask(__name__)

# temporary consumable variable, to be replaced by module's flask later 
RingSpareBayCon = 1
NonRingSpareBayCon = 1 
TempBracketCon = 1
TrayPaperCon = 1
WrappingPaperCon = 1
WrappingSealerCon = 1
PrintedListWrapperCon = 1
A4PaperCon = 1
IndicatorDispenserCon = 1
StickerTagCon = 1
ConsumablesDict = {'RingSpareBay' : RingSpareBayCon, 'NonRingSpareBay' : NonRingSpareBayCon, 'TempBracket' : TempBracketCon, 'TrayPaper' : TrayPaperCon, 'WrappingPaper' : WrappingPaperCon, 'WrappingSealer' : WrappingSealerCon, 'PrintedListWrapper' : PrintedListWrapperCon, 'A4Paper' : A4PaperCon, 'IndicatorDispenser' : IndicatorDispenserCon, 'StickerTag' : StickerTagCon}


WetBayTray = [0] * 6
WetBayDict = {'WetBayTray':WetBayTray}

DryBayCC = [0] * 6
DryBayDict = {'DryBayCC':DryBayCC}


MagilsAvailability = [0] * 12
MagilsDict = {'MagilsAvailability':MagilsAvailability}

@app.route('/CheckConsumables', methods = ['GET'])
def CheckConsumables():
    # collect all consumables data from diff modules, using hardcoded variables as of now
    # eg:
    #   for x in ConsumablesDict:
    #       data = requests.post(x + URL + /get_consumable , json = data)
    #       ConsumablesDict[x] = int(data.text)
    #
    # updateGUI() #update GUI current status
    error_list = []
    for x in ConsumablesDict:
        print("checking consumables for module: " + str(x))
        if not ConsumablesDict[x]:
            error_list.append(x)
    if len(error_list) != 0:
        s = ""
        for x in error_list:
            s += x + ', '
        print("Consumables checking failed, error in following modules: " + s)
        return '0'
    else:
        print("Consumables checking successful")
        return '1'

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

'''
PrinterStartPrinter = 0
PrinterStartWrapping = 0
PrinterBay = 0
PrinterDict = {'StartPrinter':PrinterStartPrinter, 'StartWrapping':PrinterStartWrapping}

DispenseIndicator = 0
IndicatorBay = 0
IndicatorDict = {'DispenseIndicator':DispenseIndicator}

DispenseTag = 0
StickerBay = 0
StickerDict = {'DispenseTag':DispenseTag}

WrappingStartWrapping = 0
WrappingBayPaper = 0
WrappingBayTape = 0
WrappingDict = {'StartWrapping':WrappingStartWrapping}

TrayLiftPaper = 0
TrayPaperBay = 0
TrayPaperDict= {'LiftPaper':TrayLiftPaper}

RingSpareBay = 0
RingSpareInst = {'ForcepArteryAdson': 10, 'ForcepArteryCrile':2, 'ForcepTissueStilles': 4, 'ForcepTissueBabcock': 8}
RingSpareBayDict = {'SpareInst': RingSpareInst}

NonRingSpareBay = 0
NonRingSpareInst = {'ClipTowelJones': 10, 'Retractors': 4, 'SpearRedivac': 2}
NonRingSpearLift = 0
NonRingSpareBayDict = {'SpareInst': NonRingSpareInst, 'LiftSpear': NonRingSpearLift}


IB2StartPositioner = 0
IB2ShuttleLoad = 0
IB2ShuttleUnload = 0
IB2StartInspection = 0
IB2DefectiveInst = []
IB2OngoingInst = []
IB2CompletedInst = []
IB2SystemError = 0
IB2Slot1 = 'mixed'
shuttle_1 = {'instrument': '', 'location': '', 'status': '', 'defective': 0}
shuttle_2 = {'instrument': '', 'location': '', 'status': '', 'defective': 0}
shuttle_3 = {'instrument': '', 'location': '', 'status': '', 'defective': 0}
shuttle_4 = {'instrument': '', 'location': '', 'status': '', 'defective': 0}
shuttle_5 = {'instrument': '', 'location': '', 'status': '', 'defective': 0}
shuttle_6 = {'instrument': '', 'location': '', 'status': '', 'defective': 0}
shuttle_dict = {'list': [shuttle_1, shuttle_2, shuttle_3, shuttle_4, shuttle_5, shuttle_6]}
IB2Dict = {'IB2Slot1':IB2Slot1, 'IB2Shuttle': shuttle_dict, 'StartPositioner':IB2StartPositioner, 'LoadShuttle':IB2ShuttleLoad, 'UnloadShuttle':IB2ShuttleUnload, 'StartInspection': IB2StartInspection, 'DefectiveInst':IB2DefectiveInst, 'OngoingInst':IB2OngoingInst, 'CompletedInst':IB2CompletedInst}

IB1StartFlat = 0
IB1StartTip = 0
IB1CorrectingMech = 0
IB1DefectiveInst = ['retractor', 'retractor']
IB1OngoingInst = []
IB1CompletedInst = []
IB1SystemError = 0
IB1Dict = {'StartFlat': IB1StartFlat, 'StartTip':IB1StartTip, 'CorrectingMech':IB1CorrectingMech, 'DefectiveInst':IB1DefectiveInst, 'OngoingInst':IB1OngoingInst, 'CompletedInst':IB1CompletedInst}

IndicatorLightPanel = [0, 0, 0, 0]
IndicatorLightDict = {'IndicatorLight': IndicatorLightPanel}

UR5Lock = 0
ServiceDoorLock = 0

SystemErrorDict = {'DryBayDrainSystemError':DryBayDrainSystemError, 'MagilsBay':MagilsBay, 'PrinterBay':PrinterBay, 'IndicatorDispenser':IndicatorBay, 'StickerTag':StickerBay, 'WrappingBay': [WrappingBayPaper, WrappingBayTape], 'TrayPaperBay':TrayPaperBay, 'RingSpareBay':RingSpareBay, 'NonRingSpareBay':NonRingSpareBay, 'NonRingInspectionBay':IB1SystemError, 'RingInspectionBay':IB1SystemError, 'UR5': UR5Lock, 'ServiceDoor': ServiceDoorLock}

Database = {'ConsumablesAvailability':ConsumablesDict, 'WetBay':WetBayDict, 'DryBay': DryBayDict, 'MagilsBay':MagilsDict, 'PrinterBay': PrinterDict, 'IndicatorDispenser':IndicatorDict, 'StickerTag':StickerDict, 'WrappingBay': WrappingDict, 'TrayPaperBay':TrayPaperDict, 'RingSpareBay': RingSpareBayDict, 'NonRingSpareBay': NonRingSpareBayDict, 'NonRingInspectionBay':IB1Dict, 'RingInspectionBay':IB2Dict, 'IndicatorLight': IndicatorLightDict}

def CompileDatabaseDict():
    global Database
    ConsumablesDict = {'RingSpareBay' : RingSpareBayCon, 'NonRingSpareBay' : NonRingSpareBayCon, 'TempBracket' : TempBracketCon, 'TrayPaper' : TrayPaperCon, 'WrappingPaper' : WrappingPaperCon, 'WrappingSealer' : WrappingSealerCon, 'PrintedListWrapper' : PrintedListWrapperCon, 'A4Paper' : A4PaperCon, 'IndicatorDispenser' : IndicatorDispenserCon, 'StickerTag' : StickerTagCon}
    WetBayDict = {'WetBayTray':WetBayTray, 'WetBayAirKnives':WetBayAirKnives, 'WetBayLED':WetBayLED, 'WetBayGasCylinder':WetBayGasCylinder}
    DryBayDict = {'DryBayCover':DryBayCover, 'DryBayContainer':DryBayContainer, 'DryBayGasCylinder':DryBayGasCylinder,'DryBayLED':DryBayLED}
    MagilsDict = {'MagilsAvailability':MagilsAvailability, 'DispenseMagils':DispenseMagils}
    PrinterDict = {'StartPrinter':PrinterStartPrinter, 'StartWrapping':PrinterStartWrapping}
    IndicatorDict = {'DispenseIndicator':DispenseIndicator}
    StickerDict = {'DispenseTag':DispenseTag}
    WrappingDict = {'StartWrapping':WrappingStartWrapping}
    TrayPaperDict= {'LiftPaper':TrayLiftPaper}
    RingSpareBayDict = {'SpareInst': RingSpareInst}
    NonRingSpareBayDict = {'SpareInst': NonRingSpareInst, 'LiftSpear': NonRingSpearLift}
    IB2Dict = {'IB2Slot1':IB2Slot1, 'IB2Shuttle': shuttle_dict, 'StartPositioner':IB2StartPositioner, 'LoadShuttle':IB2ShuttleLoad, 'UnloadShuttle':IB2ShuttleUnload, 'StartInspection': IB2StartInspection, 'DefectiveInst':IB2DefectiveInst, 'OngoingInst':IB2OngoingInst, 'CompletedInst':IB2CompletedInst}
    IB1Dict = {'StartFlat': IB1StartFlat, 'StartTip':IB1StartTip, 'CorrectingMech':IB1CorrectingMech, 'DefectiveInst':IB1DefectiveInst, 'OngoingInst':IB1OngoingInst, 'CompletedInst':IB1CompletedInst}
    IndicatorLightDict = {'IndicatorLight': IndicatorLightPanel}
    Database = {'ConsumablesAvailability':ConsumablesDict, 'WetBay':WetBayDict, 'DryBay': DryBayDict, 'MagilsBay':MagilsDict, 'PrinterBay': PrinterDict, 'IndicatorDispenser':IndicatorDict, 'StickerTag':StickerDict, 'WrappingBay': WrappingDict, 'TrayPaperBay':TrayPaperDict, 'RingSpareBay': RingSpareBayDict, 'NonRingSpareBay': NonRingSpareBayDict, 'NonRingInspectionBay':IB1Dict, 'RingInspectionBay':IB2Dict, 'IndicatorLight': IndicatorLightDict}

@app.route('/CheckConsumables', methods=['POST'])
def CheckConsumables():
    data = request.get_json()
    print(data['modules'])
    x = data['modules']
    return str(Database['ConsumablesAvailability'][x])

@app.route('/CheckPigeonHole', methods=['GET'])
def CheckPigeonHole():
    x = {"Tray": Database['WetBay']['WetBayTray'], "Cover": Database['DryBay']['DryBayCover'], "Container": Database['DryBay']['DryBayContainer']}
    return x

@app.route('/CheckMagils', methods=['GET'])
def CheckMagils():
    i = 0
    for x in Database['MagilsBay']['MagilsAvailability']:
        i += 1
    if i > 0:
        return "1"
    else:
        return "0"

@app.route('/FaultyInstruments', methods=['GET','POST'])
def FaultyInstruments():
    global Database, IB1DefectiveInst
    if request.method == 'GET':
        return Database['NonRingInspectionBay']
    else:
        data = request.get_json()
        if data['action'] == 'clear':
            IB1DefectiveInst = []
            CompileDatabaseDict()
            return "defective instruments list cleared"
        else:
            for x in data['instruments']:
                IB1DefectiveInst.append(x)
            return "defective instruments list updated"

@app.route('/UpdateModules', methods=['POST'])
def UpdateModules():
    pass

@app.route('/CheckAll', methods=['GET'])
def CheckAll():
    global Database
    return Database

@app.route('/Error', methods=['GET'])
def Error():
    global SystemErrorDict
    return SystemErrorDict

@app.route('/InspectionBay2', methods = ['GET', 'POST'])
def InspectionBay2():
    global shuttle_dict
    if request.method == 'GET':
        return Database['RingInspectionBay']
    else:
        data = request.get_json()
        shuttle_dict = data['shuttle_dict']
        print(data['shuttle_dict'])
        CompileDatabaseDict()
        return "True"

@app.route('/IB2FaultyInstruments', methods = ['GET'])
def IB2FaultyInstruments():
    assembly_arr = []
    for x in shuttle_dict['list']:
        assembly_arr.append(x['defective'])
    data = {'assembly_arr':assembly_arr}
    return data

@app.route('/DebugPage', methods = ['GET'])
def DebugPage():
    return render_template('index.html')

@app.route('/DebugPageStatus', methods = ['GET', 'POST'])
def DebugPageStatus():
    global WetBayTray, DryBayContainer, DryBayCover, shuttle_dict, IB1DefectiveInst
    if request.method == 'GET':

        defective_arr = 6*[0]
        for i in range(0, 6):
            defective_arr[i] = eval("shuttle_" + str(i+1))['defective']
        print(defective_arr)
        data = {'tray':WetBayTray, 'cover':DryBayCover, 'container':DryBayContainer, 'shuttle': defective_arr}
        return data
    else:
        data = request.get_json()
        print(data)
        if data['type'] == "tray":
            WetBayTray[data['position'] - 1] = data['value']
        elif data['type'] == "cover":
            DryBayCover[data['position'] - 1] = data['value']
        elif data['type'] == "container":
            DryBayContainer[data['position'] - 1] = data['value']
        elif data['type'] == "shuttle":
            shuttle_dict['list'][data['position'] - 1]['defective'] = data['value']
        elif data['type'] == "nonring":
            IB1DefectiveInst = data['value']
        print(shuttle_dict['list'])
        CompileDatabaseDict()
        print(shuttle_dict)
        return "ok"

'''
if __name__ == "__main__":
    app.run(debug=True)
