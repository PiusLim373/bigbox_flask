#!/usr/bin/env python

import rospy
import smach
import smach_ros
from smach import CBState
from time import sleep
import requests
from flask import json

IB2URL = 'http://0.0.0.0:5000/InspectionBay2'
IB2FaultyInstrumentsURL = 'http://0.0.0.0:5000/IB2FaultyInstruments'
ForcepBrac = ['artery_crile', 'artery_adson', 'artery_adson', 'artery_adson', 'artery_adson', 'artery_adson', 'artery_adson', 'artery_adson', 'artery_adson', 'artery_adson', 'artery_adson', 'artery_adson', 'artery_adson']
MixedBrac = ['mayo_hegar', 'crilewood', 'littlewood', 'littlewood', 'stilles', 'stilles','babcock', 'babcock', 'babcock', 'babcock', 'nurses', 'mayo', 'metzenbaum', 'rampley']

slot1 = ''
slot2 = ''
shuttle_count = 0
shuttle_1 = {'instrument': '', 'location': '', 'status': ''}
shuttle_2 = {'instrument': '', 'location': '', 'status': '', 'defective': 0}
shuttle_3 = {'instrument': '', 'location': '', 'status': '', 'defective': 0}
shuttle_4 = {'instrument': '', 'location': '', 'status': '', 'defective': 0}
shuttle_5 = {'instrument': '', 'location': '', 'status': '', 'defective': 0}
shuttle_6 = {'instrument': '', 'location': '', 'status': '', 'defective': 0}
shuttle_dict = {'list': [shuttle_1, shuttle_2, shuttle_3, shuttle_4, shuttle_5, shuttle_6]}
assembly_arr = [] #zero for no issue, one for defective inst
assembly_count = 0

def UpdateDefective():
    global shuttle_dict
    x = requests.get(IB2FaultyInstrumentsURL)
    jsondata = json.loads(x.content)
    arr = jsondata['assembly_arr']
    for i in range(0,6):
        shuttle_dict['list'][i]['defective'] = arr[i]
    print(assembly_arr)

def UpdateDatabase():
    data = {'shuttle_dict': shuttle_dict}
    x = requests.post(IB2URL, json = data)
    return 1

class CheckBracSM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success','fail'])
    
    def execute(self, userdata):
        global slot1, slot2
        print(assembly_arr)
        #use vision to check bracket on slot1
        # #
        x = requests.get(IB2URL)
        jsondata = json.loads(x.content)
        if jsondata['IB2Slot1'] == "mixed":
            slot1 = MixedBrac
            slot2 = ForcepBrac
        else: 
            slot1 = ForcepBrac
            slot2 = MixedBrac
        return 'success'

class TransferSlot1ShuttleSM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success','fail'])
    
    def execute(self, userdata):
        global shuttle_count, shuttle_dict
        #Transfer 1 ring insrument from slot1 to shuttle, make shuttle go for inspection after placing
        #
        PickSuccess = True
        if PickSuccess:
            UpdateDefective()
            shuttle_dict['list'][shuttle_count]['instrument'] = slot1[0]
            slot1.pop(0)
            shuttle_dict['list'][shuttle_count]['status'] = 'instrument loaded, proceeding to oilling station'
            shuttle_count += 1
            UpdateDatabase()
        return 'success'

class CheckDefectSM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success'])
    
    def execute(self, userdata):
        raw_input()
        global assembly_arr
        #request from ib2 server to check which shuttle has defective instrument
        #assuming no error for now
        x = requests.get(IB2FaultyInstrumentsURL)
        jsondata = json.loads(x.content)
        print(jsondata)
        assembly_arr = jsondata['assembly_arr']
        print(assembly_arr)
        return 'success'

class TransferShuttleSlot3SM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success', 'fail'])
    
    def execute(self, userdata):
        if assembly_count < 6:
            global assembly_arr, assembly_count
            #tranfer inst from shuttle to temp bracket (slot3)
            #if there is defective inst, transfer from spare bay instead
            if assembly_arr[assembly_count]:
                rospy.logerr("Defective ring instrument! name: " + str(shuttle_dict['list'][assembly_count]['instrument']) + ", proceed to replace from ring spare bay")
                #replacing code
                rospy.logerr("Spare instrument replaced")
                assembly_arr[assembly_count] = 0
            assembly_count += 1
            return 'success'
        else:
            rospy.logerr("All shuttle emptied, skipping this..")
            return 'success'

class ResetCounterSM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success'])
    
    def execute(self, userdata):
        raw_input()
        global assembly_arr, assembly_count, shuttle_count, shuttle_dict, shuttle_1, shuttle_2, shuttle_3, shuttle_4, shuttle_5, shuttle_6
        assembly_arr = [0, 0, 0, 0, 0, 0] 
        assembly_count = 0
        shuttle_count = 0
        shuttle_1 = {'instrument': '', 'location': '', 'status': '', 'defective': 0}
        shuttle_2 = {'instrument': '', 'location': '', 'status': '', 'defective': 0}
        shuttle_3 = {'instrument': '', 'location': '', 'status': '', 'defective': 0}
        shuttle_4 = {'instrument': '', 'location': '', 'status': '', 'defective': 0}
        shuttle_5 = {'instrument': '', 'location': '', 'status': '', 'defective': 0}
        shuttle_6 = {'instrument': '', 'location': '', 'status': '', 'defective': 0}
        shuttle_dict = {'list': [shuttle_1, shuttle_2, shuttle_3, shuttle_4, shuttle_5, shuttle_6]}

        
        return 'success'

class CheckSlot1SM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['forcep', 'mixed'])
    
    def execute(self, userdata):
        #check if slot1 is mixbracket or forcepbracket (forcep brac has 13 inst while mix has 14 inst)
        if slot1 == MixedBrac:
            return 'mixed'
        else: 
            return 'forcep'

class TransferSlot2ShuttleSM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success','fail'])
    
    def execute(self, userdata):
        if shuttle_count < 6:
            global shuttle_count, shuttle_dict
            #Transfer 1 ring insrument from slot2 to shuttle, make shuttle go for inspection after placing
            #
            PickSuccess = True
            if PickSuccess:
                shuttle_dict['list'][shuttle_count]['instrument'] = slot2[0]
                slot2.pop(0)
                shuttle_dict['list'][shuttle_count]['status'] = 'instrument loaded, proceeding to oilling station'
                shuttle_count += 1
                UpdateDatabase()
            return 'success'
        else:
            rospy.logerr("Shuttle full, skipping loading process")
            return 'success'

class TransferShuttleSlot1SM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success', 'fail'])
    
    def execute(self, userdata):
        global assembly_arr, assembly_count
        #tranfer inst from shuttle to second bracket (slot1)
        #if there is defective inst, transfer from spare bay instead
        if assembly_arr[assembly_count]:
            rospy.logerr("Defective ring instrument! name: " + str(shuttle_dict['list'][assembly_count]['instrument']) + ", proceed to replace from ring spare bay")
            #replacing code
            rospy.logerr("Spare instrument replaced")
            assembly_arr[assembly_count] = 0
        assembly_count += 1
        return 'success'

class ShiftTempBracSM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success', 'fail'])
    
    def execute(self, userdata):
        #trasnfer empty slot 2 brac to slot 3 for the next cycle
        #include code to move arm here
        return 'success'

def main():
    rospy.init_node("ur5flowb")
    sm = smach.StateMachine(outcomes = ['ended'])
    with sm:
        smach.StateMachine.add('CheckBracSM', CheckBracSM(), transitions={'success':'TransferSlot1ShuttleSM_1', 'fail':'CheckBracSM'})
        smach.StateMachine.add('TransferSlot1ShuttleSM_1', TransferSlot1ShuttleSM(), transitions={'success':'TransferSlot1ShuttleSM_2', 'fail':'TransferSlot1ShuttleSM_1'})
        smach.StateMachine.add('TransferSlot1ShuttleSM_2', TransferSlot1ShuttleSM(), transitions={'success':'TransferSlot1ShuttleSM_3', 'fail':'TransferSlot1ShuttleSM_2'})
        smach.StateMachine.add('TransferSlot1ShuttleSM_3', TransferSlot1ShuttleSM(), transitions={'success':'TransferSlot1ShuttleSM_4', 'fail':'TransferSlot1ShuttleSM_3'})
        smach.StateMachine.add('TransferSlot1ShuttleSM_4', TransferSlot1ShuttleSM(), transitions={'success':'TransferSlot1ShuttleSM_5', 'fail':'TransferSlot1ShuttleSM_4'})
        smach.StateMachine.add('TransferSlot1ShuttleSM_5', TransferSlot1ShuttleSM(), transitions={'success':'TransferSlot1ShuttleSM_6', 'fail':'TransferSlot1ShuttleSM_5'})
        smach.StateMachine.add('TransferSlot1ShuttleSM_6', TransferSlot1ShuttleSM(), transitions={'success':'CheckDefectSM_1', 'fail':'TransferSlot1ShuttleSM_6'})
        smach.StateMachine.add('CheckDefectSM_1', CheckDefectSM(), transitions={'success':'TransferShuttleSlot3SM_1'})
        smach.StateMachine.add('TransferShuttleSlot3SM_1', TransferShuttleSlot3SM(), transitions={'success':'TransferShuttleSlot3SM_2', 'fail':'TransferShuttleSlot3SM_1'})
        smach.StateMachine.add('TransferShuttleSlot3SM_2', TransferShuttleSlot3SM(), transitions={'success':'TransferShuttleSlot3SM_3', 'fail':'TransferShuttleSlot3SM_2'})
        smach.StateMachine.add('TransferShuttleSlot3SM_3', TransferShuttleSlot3SM(), transitions={'success':'TransferShuttleSlot3SM_4', 'fail':'TransferShuttleSlot3SM_3'})
        smach.StateMachine.add('TransferShuttleSlot3SM_4', TransferShuttleSlot3SM(), transitions={'success':'TransferShuttleSlot3SM_5', 'fail':'TransferShuttleSlot3SM_4'})
        smach.StateMachine.add('TransferShuttleSlot3SM_5', TransferShuttleSlot3SM(), transitions={'success':'TransferShuttleSlot3SM_6', 'fail':'TransferShuttleSlot3SM_5'})
        smach.StateMachine.add('TransferShuttleSlot3SM_6', TransferShuttleSlot3SM(), transitions={'success':'ResetCounterSM_1', 'fail':'TransferShuttleSlot3SM_6'})
        smach.StateMachine.add('ResetCounterSM_1', ResetCounterSM(), transitions={'success':'TransferSlot1ShuttleSM_7'})
        smach.StateMachine.add('TransferSlot1ShuttleSM_7', TransferSlot1ShuttleSM(), transitions={'success':'TransferSlot1ShuttleSM_8', 'fail':'TransferSlot1ShuttleSM_7'})
        smach.StateMachine.add('TransferSlot1ShuttleSM_8', TransferSlot1ShuttleSM(), transitions={'success':'TransferSlot1ShuttleSM_9', 'fail':'TransferSlot1ShuttleSM_8'})
        smach.StateMachine.add('TransferSlot1ShuttleSM_9', TransferSlot1ShuttleSM(), transitions={'success':'TransferSlot1ShuttleSM_10', 'fail':'TransferSlot1ShuttleSM_9'})
        smach.StateMachine.add('TransferSlot1ShuttleSM_10', TransferSlot1ShuttleSM(), transitions={'success':'TransferSlot1ShuttleSM_11', 'fail':'TransferSlot1ShuttleSM_10'})
        smach.StateMachine.add('TransferSlot1ShuttleSM_11', TransferSlot1ShuttleSM(), transitions={'success':'TransferSlot1ShuttleSM_12', 'fail':'TransferSlot1ShuttleSM_11'})
        smach.StateMachine.add('TransferSlot1ShuttleSM_12', TransferSlot1ShuttleSM(), transitions={'success':'CheckDefectSM_2', 'fail':'TransferSlot1ShuttleSM_12'})
        smach.StateMachine.add('CheckDefectSM_2', CheckDefectSM(), transitions={'success':'TransferShuttleSlot3SM_7'})
        smach.StateMachine.add('TransferShuttleSlot3SM_7', TransferShuttleSlot3SM(), transitions={'success':'TransferShuttleSlot3SM_8', 'fail':'TransferShuttleSlot3SM_7'})
        smach.StateMachine.add('TransferShuttleSlot3SM_8', TransferShuttleSlot3SM(), transitions={'success':'TransferShuttleSlot3SM_9', 'fail':'TransferShuttleSlot3SM_8'})
        smach.StateMachine.add('TransferShuttleSlot3SM_9', TransferShuttleSlot3SM(), transitions={'success':'TransferShuttleSlot3SM_10', 'fail':'TransferShuttleSlot3SM_9'})
        smach.StateMachine.add('TransferShuttleSlot3SM_10', TransferShuttleSlot3SM(), transitions={'success':'TransferShuttleSlot3SM_11', 'fail':'TransferShuttleSlot3SM_10'})
        smach.StateMachine.add('TransferShuttleSlot3SM_11', TransferShuttleSlot3SM(), transitions={'success':'TransferShuttleSlot3SM_12', 'fail':'TransferShuttleSlot3SM_11'})
        smach.StateMachine.add('TransferShuttleSlot3SM_12', TransferShuttleSlot3SM(), transitions={'success':'ResetCounterSM_2', 'fail':'TransferShuttleSlot3SM_12'})
        smach.StateMachine.add('ResetCounterSM_2', ResetCounterSM(), transitions={'success':'TransferSlot1ShuttleSM_13'})
        smach.StateMachine.add('TransferSlot1ShuttleSM_13', TransferSlot1ShuttleSM(), transitions={'success':'CheckSlot1SM', 'fail':'TransferSlot1ShuttleSM_13'})
        smach.StateMachine.add('CheckSlot1SM', CheckSlot1SM(), transitions={'forcep':'TransferSlot2ShuttleSM_1', 'mixed':'TransferSlot1ShuttleSM_14'})
        smach.StateMachine.add('TransferSlot1ShuttleSM_14', TransferSlot1ShuttleSM(), transitions={'success':'TransferSlot2ShuttleSM_1', 'fail':'TransferSlot1ShuttleSM_14'})
        smach.StateMachine.add('TransferSlot2ShuttleSM_1', TransferSlot2ShuttleSM(), transitions={'success':'TransferSlot2ShuttleSM_2', 'fail':'TransferSlot2ShuttleSM_1'})
        smach.StateMachine.add('TransferSlot2ShuttleSM_2', TransferSlot2ShuttleSM(), transitions={'success':'TransferSlot2ShuttleSM_3', 'fail':'TransferSlot2ShuttleSM_2'})
        smach.StateMachine.add('TransferSlot2ShuttleSM_3', TransferSlot2ShuttleSM(), transitions={'success':'TransferSlot2ShuttleSM_4', 'fail':'TransferSlot2ShuttleSM_3'})
        smach.StateMachine.add('TransferSlot2ShuttleSM_4', TransferSlot2ShuttleSM(), transitions={'success':'TransferSlot2ShuttleSM_5', 'fail':'TransferSlot2ShuttleSM_4'})
        smach.StateMachine.add('TransferSlot2ShuttleSM_5', TransferSlot2ShuttleSM(), transitions={'success':'CheckDefectSM_3', 'fail':'TransferSlot2ShuttleSM_5'})
        smach.StateMachine.add('CheckDefectSM_3', CheckDefectSM(), transitions={'success':'TransferShuttleSlot3SM_13'})
        smach.StateMachine.add('TransferShuttleSlot3SM_13', TransferShuttleSlot3SM(), transitions={'success':'CheckTempBracSM', 'fail':'TransferShuttleSlot3SM_13'})
        smach.StateMachine.add('CheckTempBracSM', CheckSlot1SM(), transitions={'forcep':'TransferShuttleSlot1SM_1', 'mixed':'TransferShuttleSlot3SM_14'})
        smach.StateMachine.add('TransferShuttleSlot3SM_14', TransferShuttleSlot3SM(), transitions={'success':'TransferShuttleSlot1SM_1', 'fail':'TransferShuttleSlot3SM_14'})
        smach.StateMachine.add('TransferShuttleSlot1SM_1', TransferShuttleSlot3SM(), transitions={'success':'TransferShuttleSlot1SM_2', 'fail':'TransferShuttleSlot1SM_1'})
        smach.StateMachine.add('TransferShuttleSlot1SM_2', TransferShuttleSlot3SM(), transitions={'success':'TransferShuttleSlot1SM_3', 'fail':'TransferShuttleSlot1SM_2'})
        smach.StateMachine.add('TransferShuttleSlot1SM_3', TransferShuttleSlot3SM(), transitions={'success':'TransferShuttleSlot1SM_4', 'fail':'TransferShuttleSlot1SM_3'})
        smach.StateMachine.add('TransferShuttleSlot1SM_4', TransferShuttleSlot3SM(), transitions={'success':'TransferShuttleSlot1SM_5', 'fail':'TransferShuttleSlot1SM_4'})
        smach.StateMachine.add('TransferShuttleSlot1SM_5', TransferShuttleSlot3SM(), transitions={'success':'ResetCounterSM_3', 'fail':'TransferShuttleSlot1SM_5'})
        smach.StateMachine.add('ResetCounterSM_3', ResetCounterSM(), transitions={'success':'TransferSlot2ShuttleSM_6'})
        smach.StateMachine.add('TransferSlot2ShuttleSM_6', TransferSlot2ShuttleSM(), transitions={'success':'TransferSlot2ShuttleSM_7', 'fail':'TransferSlot2ShuttleSM_6'})
        smach.StateMachine.add('TransferSlot2ShuttleSM_7', TransferSlot2ShuttleSM(), transitions={'success':'TransferSlot2ShuttleSM_8', 'fail':'TransferSlot2ShuttleSM_7'})
        smach.StateMachine.add('TransferSlot2ShuttleSM_8', TransferSlot2ShuttleSM(), transitions={'success':'TransferSlot2ShuttleSM_9', 'fail':'TransferSlot2ShuttleSM_8'})
        smach.StateMachine.add('TransferSlot2ShuttleSM_9', TransferSlot2ShuttleSM(), transitions={'success':'TransferSlot2ShuttleSM_10', 'fail':'TransferSlot2ShuttleSM_9'})
        smach.StateMachine.add('TransferSlot2ShuttleSM_10', TransferSlot2ShuttleSM(), transitions={'success':'TransferSlot2ShuttleSM_11', 'fail':'TransferSlot2ShuttleSM_10'})
        smach.StateMachine.add('TransferSlot2ShuttleSM_11', TransferSlot2ShuttleSM(), transitions={'success':'CheckDefectSM_4', 'fail':'TransferSlot2ShuttleSM_11'})
        smach.StateMachine.add('CheckDefectSM_4', CheckDefectSM(), transitions={'success':'TransferShuttleSlot1SM_6'})
        smach.StateMachine.add('TransferShuttleSlot1SM_6', TransferShuttleSlot3SM(), transitions={'success':'TransferShuttleSlot1SM_7', 'fail':'TransferShuttleSlot1SM_6'})
        smach.StateMachine.add('TransferShuttleSlot1SM_7', TransferShuttleSlot3SM(), transitions={'success':'TransferShuttleSlot1SM_8', 'fail':'TransferShuttleSlot1SM_7'})
        smach.StateMachine.add('TransferShuttleSlot1SM_8', TransferShuttleSlot3SM(), transitions={'success':'TransferShuttleSlot1SM_9', 'fail':'TransferShuttleSlot1SM_8'})
        smach.StateMachine.add('TransferShuttleSlot1SM_9', TransferShuttleSlot3SM(), transitions={'success':'TransferShuttleSlot1SM_10', 'fail':'TransferShuttleSlot1SM_9'})
        smach.StateMachine.add('TransferShuttleSlot1SM_10', TransferShuttleSlot3SM(), transitions={'success':'TransferShuttleSlot1SM_11', 'fail':'TransferShuttleSlot1SM_10'})
        smach.StateMachine.add('TransferShuttleSlot1SM_11', TransferShuttleSlot3SM(), transitions={'success':'ResetCounterSM_4', 'fail':'TransferShuttleSlot1SM_11'})
        smach.StateMachine.add('ResetCounterSM_4', ResetCounterSM(), transitions={'success':'TransferSlot2ShuttleSM_12'})
        smach.StateMachine.add('TransferSlot2ShuttleSM_12', TransferSlot2ShuttleSM(), transitions={'success':'TransferSlot2ShuttleSM_13', 'fail':'TransferSlot2ShuttleSM_12'})
        smach.StateMachine.add('TransferSlot2ShuttleSM_13', TransferSlot2ShuttleSM(), transitions={'success':'TransferSlot2ShuttleSM_14', 'fail':'TransferSlot2ShuttleSM_13'})
        smach.StateMachine.add('TransferSlot2ShuttleSM_14', TransferSlot2ShuttleSM(), transitions={'success':'CheckDefectSM_5', 'fail':'TransferSlot2ShuttleSM_14'})
        smach.StateMachine.add('CheckDefectSM_5', CheckDefectSM(), transitions={'success':'TransferShuttleSlot1SM_12'})
        smach.StateMachine.add('TransferShuttleSlot1SM_12', TransferShuttleSlot3SM(), transitions={'success':'TransferShuttleSlot1SM_13', 'fail':'TransferShuttleSlot1SM_12'})
        smach.StateMachine.add('TransferShuttleSlot1SM_13', TransferShuttleSlot3SM(), transitions={'success':'TransferShuttleSlot1SM_14', 'fail':'TransferShuttleSlot1SM_13'})
        smach.StateMachine.add('TransferShuttleSlot1SM_14', TransferShuttleSlot3SM(), transitions={'success':'ResetCounterSM_5', 'fail':'TransferShuttleSlot1SM_14'})
        smach.StateMachine.add('ResetCounterSM_5', ResetCounterSM(), transitions={'success':'ShiftTempBracSM'})
        smach.StateMachine.add('ShiftTempBracSM', ShiftTempBracSM(), transitions={'success':'ended', 'fail':'ShiftTempBracSM'})

        #todolist: check defect with database
    
    smach_viewer = smach_ros.IntrospectionServer('bigbox_smach_server', sm, '/Start')
    smach_viewer.start()

    outcome = sm.execute()
    rospy.spin()
    smach_viewer.stop()   

if __name__ == '__main__':
    main()
    # UpdateDatabase()
    # print(shuttle_dict)
    # defectfromdb()