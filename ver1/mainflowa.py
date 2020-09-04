#!/usr/bin/env python

import rospy
import smach
import smach_ros
from smach import CBState
from time import sleep
import requests
from flask import json

url = 'http://0.0.0.0:5000'
# print(config.CheckInstruments())
CheckConsumablesURL = url + "/CheckConsumables"
CheckPigeonHoleURL = url + "/CheckPigeonHole"
CheckMagilsURL = url + "/CheckMagils"
FaultyInstURL = url + "/FaultyInstruments"

pigeonhole_to_process = []
pigeonhole_to_process_detail = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
pigeonhole_processing = 0



def checkconsumables(modules):
    data = {'modules': modules}
    x = requests.post(CheckConsumablesURL , json = data)
    return int(x.text)

def checkpigeonhole():
    global pigeonhole_to_process, pigeonhole_processing
    pigeonhole_to_process = []
    x = requests.get(CheckPigeonHoleURL)
    jsondata = json.loads(x.content)
    tray = jsondata['Tray']
    cover = jsondata['Cover']
    container = jsondata['Container']
    for i in range(1,7):
        if (tray[i-1] == 1 and cover [i-1] == 1 and container[i-1] == 1):
            pigeonhole_to_process_detail[i-1] = [1, 1, 1]
            pigeonhole_to_process.append(i)
        else: 
            pigeonhole_to_process_detail[i-1][0] = tray[i-1]
            pigeonhole_to_process_detail[i-1][1] = cover[i-1]
            pigeonhole_to_process_detail[i-1][2] = container[i-1]
    pigeonhole_processing = pigeonhole_to_process[0]
    return pigeonhole_to_process

###SETUP  
class CheckConsumablesSM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success','fail'])
    
    def execute(self, userdata):
        error_list = []
        rospy.loginfo("Checking Ring Spare Bay...")
        if not checkconsumables("RingSpareBay"):
            error_list.append("Ring Spare Bay")
        rospy.loginfo("Checking Non-Ring Spare Bay...")
        if not checkconsumables("NonRingSpareBay"):
            error_list.append("Non Ring Spare Bay")
        rospy.loginfo("Checking Temp Bracket...")
        if not checkconsumables("TempBracket"):
            error_list.append("Temp Bracket")
        rospy.loginfo("Checking Tray Paper (50cm*30cm)...")
        if not checkconsumables("TrayPaper"):
            error_list.append("Tray Paper (50cm*30cm)")
        rospy.loginfo("Checking Wrapping Paper (30cm*30cm)...")
        if not checkconsumables("WrappingPaper"):
            error_list.append("Wrapping Paper (30cm*30cm)")
        rospy.loginfo("Checking Wrapping Sealer (3M Tape)...")
        if not checkconsumables("WrappingSealer"):
            error_list.append("Wrapping Sealer (3M Tape)")
        rospy.loginfo("Checking Printed List Wrapper (30cm*30cm.)..")
        if not checkconsumables("PrintedListWrapper"):
            error_list.append("Printed List Wrapper (30cm*30cm.)")
        rospy.loginfo("Checking A4 Paper...")
        if not checkconsumables("A4Paper"):
            error_list.append("A4 Paper")
        rospy.loginfo("Checking Indicator Dispensor...")
        if not checkconsumables("IndicatorDispenser"):
            error_list.append("Indicator")
        rospy.loginfo("Checking Sticker Tag Printer...")
        if not checkconsumables("StickerTag"):
            error_list.append("Sticker Tag")

        if len(error_list) != 0:
            s = ""
            for x in error_list:
                s += x + ', '
            rospy.logerr("Consumables checking failed, error in following modules: " + s)
            return 'fail'
        else:
            rospy.loginfo("Consumables checking successful")
            return 'success'

class CheckTrayCoverContainerSM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success', 'fail'])

    def execute(self, userdata):
        global pigeonhole_to_process, pigeonhole_to_process_detail
        checkpigeonhole()
        rospy.loginfo("Checking WetBay Tray...")
        arr = [1,2,3,4,5,6]
        for x in pigeonhole_to_process:
            arr.remove(x)
        false_err_count = 0
        if len(arr) != 0:
            for x in arr:
                if (pigeonhole_to_process_detail[x-1][0] == 0 and pigeonhole_to_process_detail[x-1][1] == 0 and pigeonhole_to_process_detail[x-1][2] == 0):
                    false_err_count += 1
                else:
                    if(pigeonhole_to_process_detail[x-1][0] == 0):
                        rospy.logerr("Loading incomeplete, Pigeon hole " + str(x) + " has no Tray")
                    if(pigeonhole_to_process_detail[x-1][1] == 0):
                        rospy.logerr("Loading incomeplete, Pigeon hole " + str(x) + " has no Cover")
                    if(pigeonhole_to_process_detail[x-1][2] == 0):
                        rospy.logerr("Loading incomeplete, Pigeon hole " + str(x) + " has no Container")
        if false_err_count == len(arr):
            rospy.loginfo("Check successful")
            return 'success'
        else:
            rospy.logerr("Checking failed, please load in content as instructed")
            sleep(2)
            return 'fail'

class CheckMagilsTubeSM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success', 'fail'])

    def execute(self, userdata):
        rospy.loginfo("Checking Magils Tube Bay...")
        x = requests.get(CheckMagilsURL)
        if int(x.content):
            rospy.loginfo("Checking successful")
            rospy.loginfo("Press 'Enter' to begin....")
            raw_input()
            return 'success'
        else:
            rospy.logerr("Checking failed, please load Magils Tube in Magils input bay")
            sleep(2)
            return 'fail'
###SETUP ENDS HERE
###MAINFLOW A STARTS HERE
class ActivateAirKnifeSM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success'])

    def execute(self, userdata):
        global pigeonhole_processing
        rospy.loginfo("Activating Air knife for pigeon hole no " + str(pigeonhole_processing) + " inwards...")
        #Turn on air knife code here 
        #
        sleep(1)
        rospy.loginfo("Air knife activated successful")
        return 'success'

class ExtendWetBaySM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success'])

    def execute(self, userdata):
        global pigeonhole_processing
        rospy.loginfo("Extending WetBay pigeonhole no " + str(pigeonhole_processing) + " inwards...")
        #Turn on wetbay pigeon hole gas cylinder code here
        #
        sleep(1)
        rospy.loginfo("Extension completed")
        return 'success'

class TransferBracPT2SM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success', 'fail'])
        self.success = True

    def execute(self, userdata):
        rospy.loginfo("Transferring Forcep Bracket and Mix Bracket to Processing Table 2...")
        #read camera feed and transfer 2 ring bracket to pt2 code here
        #
        sleep(2)
        if self.success:
            rospy.loginfo("Transfer completed")
            return 'success'
        else:
            self.success = ErrorRecovery(self.success)
            return 'fail'

class ActivateUR5FlowBSM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success'])

    def execute(self, userdata):
        #Activate ur5 controller and run smach on the machine
        #
        return 'success'

class TransferKDPT1SM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success', 'fail'])
        self.success = True

    def execute(self, userdata):
        rospy.loginfo("Transferring Kidney Dish to Processing Table 1 and empyting its content...")
        #read camera feed and transfer kidney dish to pt1 code here
        #
        sleep(2)
        if self.success:
            rospy.loginfo("Transfer completed")
            return 'success'
        else:
            self.success = ErrorRecovery(self.success)
            return 'fail'

class TransferGPPT1SM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success', 'fail'])
        self.success = True

    def execute(self, userdata):
        rospy.loginfo("Transferring Gallipot to Processing Table 1...")
        #read camera feed and transfer Gallipot to pt1 code here
        #
        sleep(2)
        if self.success:
            rospy.loginfo("Transfer completed")
            return 'success'
        else:
            self.success = ErrorRecovery(self.success)
            return 'fail'

class TransferRectIB1SM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success', 'fail'])
        self.success = True

    def execute(self, userdata):
        rospy.loginfo("Transferring 1 Retractor to Inspection Bay 1...")
        #read camera feed and transfer Retractor to ib1 code here
        #
        sleep(2)
        if self.success:
            rospy.loginfo("Transfer completed")
            return 'success'
        else:
            self.success = ErrorRecovery(self.success)
            return 'fail'

class ActivateTipInspCSM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success'])

    def execute(self, userdata):
        #Activate inspection bay 1
        #
        return 'success'

class ActivateFlatInspDSM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success'])

    def execute(self, userdata):
        #Activate inspection bay 1
        #
        return 'success'

class TransferTPWBSM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success', 'fail'])
        self.success = True

    def execute(self, userdata):
        rospy.loginfo("Transferring Tray Paper to WetBay...")
        #read camera feed and tray paper to wetbay code here
        #
        sleep(2)
        if self.success:
            rospy.loginfo("Transfer completed")
            return 'success'
        else:
            self.success = ErrorRecovery(self.success)
            return 'fail'

class ExtendDryBaySM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success'])

    def execute(self, userdata):
        global pigeonhole_processing
        rospy.loginfo("Extending DryBay pigeonhole no " + str(pigeonhole_processing) + " inwards...")
        #Turn on drybay pigeon hole gas cylinder code here
        #
        sleep(1)
        rospy.loginfo("Extension completed")
        return 'success'

class TransferTrayDBSM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success', 'fail'])
        self.success = True

    def execute(self, userdata):
        rospy.loginfo("Transferring Tray to DryBay...")
        #read camera feed and tray to drybay code here
        #
        sleep(2)
        if self.success:
            rospy.loginfo("Transfer completed")
            return 'success'
        else:
            self.success = ErrorRecovery(self.success)
            return 'fail'

class RetractWetBaySM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success'])

    def execute(self, userdata):
        global pigeonhole_processing
        rospy.loginfo("Retracting WetBay pigeonhole no " + str(pigeonhole_processing) + " inwards...")
        #Turn off wetbay pigeon hole gas cylinder code here
        #
        sleep(1)
        rospy.loginfo("Retraction completed")
        return 'success'

class TransferIndiDBSM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success', 'fail'])
        self.success = True

    def execute(self, userdata):
        rospy.loginfo("Transferring 1 Indicator to DryBay...")
        #read camera feed and transfer 1 indicator to drybay code here
        #
        sleep(2)
        if self.success:
            rospy.loginfo("Transfer completed")
            return 'success'
        else:
            self.success = ErrorRecovery(self.success)
            return 'fail'

class WaitRect(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success', 'fail'])
        self.success = True

    def execute(self, userdata):
        rospy.loginfo("Waiting for Retractors inspection to complete...")
        #Insert checking code here
        #
        if self.success:
            rospy.loginfo("Transfer completed")
            return 'success'
        else:
            sleep(2)
            return 'fail'

class TransferRectDBSM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success', 'fail'])
        self.success = True

    def execute(self, userdata):
        rospy.loginfo("Transferring 2x inspected Retractors to DryBay...")
        #read camera feed and transfer 2x inspected retractors to drybay code here
        #
        sleep(2)
        if self.success:
            rospy.loginfo("Transfer completed")
            return 'success'
        else:
            self.success = ErrorRecovery(self.success)
            return 'fail'

class TransferCJIB1SM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success', 'fail'])
        self.success = True

    def execute(self, userdata):
        rospy.loginfo("Transferring 1x Towel Clip Jones to DryBay...")
        #read camera feed and transfer 1x inspected Towel Clip Jones to ib1 code here
        #
        sleep(2)
        if self.success:
            rospy.loginfo("Transfer completed")
            return 'success'
        else:
            self.success = ErrorRecovery(self.success)
            return 'fail'

class TransferGPDBSM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success', 'fail'])
        self.success = True

    def execute(self, userdata):
        rospy.loginfo("Transferring Gallipot to DryBay...")
        #read camera feed and transfer Gallipot to DryBay code here
        #
        sleep(2)
        if self.success:
            rospy.loginfo("Transfer completed")
            return 'success'
        else:
            self.success = ErrorRecovery(self.success)
            return 'fail'

class TransferKDDBSM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success', 'fail'])
        self.success = True

    def execute(self, userdata):
        rospy.loginfo("Transferring KidneyDish to DryBay...")
        #read camera feed and transfer kidneyDish to DryBay code here
        #
        sleep(2)
        if self.success:
            rospy.loginfo("Transfer completed")
            return 'success'
        else:
            self.success = ErrorRecovery(self.success)
            return 'fail'

class TransferLIIB1SM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success', 'fail'])
        self.success = True

    def execute(self, userdata):
        rospy.loginfo("Transferring 1 x loose instrument to DryBay...")
        #get data from camera about picking sequence
        #read camera feed and transfer 1 x loose instrument to IB1 code here
        #
        sleep(2)
        if self.success:
            rospy.loginfo("Transfer completed")
            return 'success'
        else:
            self.success = ErrorRecovery(self.success)
            return 'fail'

class FaultyInst(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success', 'fail'])

    def execute(self, userdata):
    # def execute(self):
        rospy.loginfo("Check for faulty instrument...")
        req = requests.get(FaultyInstURL)
        req_data = json.loads(req.content)

        while len(req_data['DefectiveInst']) != 0:
            rospy.logwarn("Faulty instument detected by Inspection Bay, list: " + str(req_data['DefectiveInst']))
            rospy.logwarn("Proceeding to replace faulty instrument...")
            for x in req_data['DefectiveInst']:
                if x == 'retractor':
                    rospy.logwarn("Replacing retractor from Spare Bay to Dry Bay...")
                    #Insert ur10 trasnfer code here, sb to db
                    #
                else:
                    rospy.logwarn("Replacing " + x +" from Spare Bay to Inspection Bay 1...")
                    #Insert ur10 trasnfer code here, sb to ib1
                    #
                success = True
                if not success:
                    self.success = ErrorRecovery(self.success)
                    return 'fail'
                else:
                    req_data['DefectiveInst'].remove(x)
        data = {'action':'clear'}
        requests.post(FaultyInstURL, json = data)
        return 'success'

class DispenseMagilSM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success'])

    def execute(self, userdata):
        #Activate magil input bay to dispense 1 x magil tube and stillet
        #
        return 'success'

class WaitTempBracket(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success', 'fail'])
        self.success = True

    def execute(self, userdata):
        rospy.loginfo("Waiting for TempBracket assembly to complete...")
        #Insert checking code here
        #
        if self.success:
            rospy.loginfo("Temp Bracket assembly completed, proceed to transferring to drybay")
            return 'success'
        else:
            sleep(2)
            return 'fail'

class TransferTBDBSM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success', 'fail'])
        self.success = True

    def execute(self, userdata):
        rospy.loginfo("Transferring Temp Bracket to DryBay...")
        #read camera feed and transfer temp bracket to drybay code here
        #
        sleep(2)
        if self.success:
            rospy.loginfo("Transfer completed")
            return 'success'
        else:
            self.success = ErrorRecovery(self.success)
            return 'fail'

class WaitSecondBracket(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success', 'fail'])
        self.success = True

    def execute(self, userdata):
        rospy.loginfo("Waiting for SecondBracket assembly to complete...")
        #Insert checking code here
        #
        if self.success:
            rospy.loginfo("SecondBracket assembly completed, proceed to transferring to drybay")
            return 'success'
        else:
            sleep(2)
            return 'fail'

class TransferSBDBSM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success', 'fail'])
        self.success = True

    def execute(self, userdata):
        rospy.loginfo("Transferring Second Bracket to DryBay...")
        #read camera feed and transfer second bracket to drybay code here
        #
        sleep(2)
        if self.success:
            rospy.loginfo("Transfer completed")
            return 'success'
        else:
            self.success = ErrorRecovery(self.success)
            return 'fail'

class TransferWPDBSM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success', 'fail'])
        self.success = True

    def execute(self, userdata):
        rospy.loginfo("Transferring wrapped package to DryBay...")
        #read camera feed and transfer wrapped package to drybay code here
        #
        sleep(2)
        if self.success:
            rospy.loginfo("Transfer completed")
            return 'success'
        else:
            self.success = ErrorRecovery(self.success)
            return 'fail'

class ActivatePBSTSM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success'])

    def execute(self, userdata):
        #Activate printer bay and sicker tag machine with info gathered
        #
        return 'success'

class TransferWPLDBSM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success', 'fail'])
        self.success = True

    def execute(self, userdata):
        rospy.loginfo("Transferring wrapped printed list to DryBay...")
        #read camera feed and transfer wrapped printed list to drybay code here
        #
        sleep(2)
        if self.success:
            rospy.loginfo("Transfer completed")
            return 'success'
        else:
            self.success = ErrorRecovery(self.success)
            return 'fail'

class TransferSTDBSM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success', 'fail'])
        self.success = True

    def execute(self, userdata):
        rospy.loginfo("Transferring sticker tag to DryBay...")
        #read camera feed and transfer sticker tag to drybay code here
        #
        sleep(2)
        if self.success:
            rospy.loginfo("Transfer completed")
            return 'success'
        else:
            self.success = ErrorRecovery(self.success)
            return 'fail'

class RetractDryBaySM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success'])

    def execute(self, userdata):
        global pigeonhole_processing
        rospy.loginfo("Retracting DryBay pigeonhole no " + str(pigeonhole_processing) + " inwards...")
        #Turn off Drybay pigeon hole gas cylinder code here
        #
        sleep(1)
        rospy.loginfo("Retraction completed")
        return 'success'







class CheckAllSetProccessedSM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success', 'fail'])
        self.counter = 1

    def execute(self, userdata):
        global pigeonhole_to_process, pigeonhole_processing
        rospy.loginfo("Pigeon hole no: " + str(pigeonhole_processing) + " process completed successfully")
        if self.counter < len(pigeonhole_to_process):
            pigeonhole_processing = pigeonhole_to_process[self.counter]
            rospy.loginfo("Next pigeon hole to process: " + str(pigeonhole_processing) )
            self.counter += 1
            return 'fail'
        else:
            rospy.loginfo("All pigeon hole has been processed!")
            return 'success'

###MAINFLOW A ENDS HERE
###ERROR RECOVERY START HER
def ErrorRecovery(arg):
    rospy.logwarn("Reaches Error Recovery function")
    #fix error here
    #
    sleep(1)
    rospy.logwarn("Error fixed, continuing")
    arg = True
    return True
###ERROR RECOVERY ENDS HERE   

class UR5FlowBSM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success'])

    def execute(self, userdata):
        return 'success'



def main():
    global pigeonhole_to_process_detail, pigeonhole_to_process
    rospy.init_node("bigbox_smach")
    sm = smach.StateMachine(outcomes=['ended'])
    # sm.userdata.pigeonhole_to_process = checkpigeonhole()
    # sm.userdata.pigeonhole_to_process_detail = pigeonhole_to_process_detail
    # sm.userdata.pigeonhole_processing = sm.userdata.pigeonhole_to_process[0]
    with sm:
        smach.StateMachine.add('CheckConsumablesSM', CheckConsumablesSM(), transitions={'success':'CheckWetDryMagilSM', 'fail':'ended'})
        CheckWetDryMagilSM = smach.StateMachine(outcomes=['success'])
        with CheckWetDryMagilSM:
            smach.StateMachine.add('CheckTrayCoverContainerSM', CheckTrayCoverContainerSM(), transitions={'success':'CheckMagilsTubeSM', 'fail':'CheckTrayCoverContainerSM'},)
            smach.StateMachine.add('CheckMagilsTubeSM', CheckMagilsTubeSM(), transitions={'success':'success', 'fail':'CheckMagilsTubeSM'})
        smach.StateMachine.add('CheckWetDryMagilSM', CheckWetDryMagilSM, transitions={'success':'MainFlowASM'})
        MainFlowASM = smach.StateMachine(outcomes=['success'])
        with MainFlowASM:
            smach.StateMachine.add('ActivateAirKnifeSM', ActivateAirKnifeSM(), transitions={'success':'ExtendWetBaySM'})
            smach.StateMachine.add('ExtendWetBaySM', ExtendWetBaySM(), transitions={'success':'TransferBracPT2SM'})
            smach.StateMachine.add('TransferBracPT2SM', TransferBracPT2SM(), transitions={'success':'ActivateUR5FlowBSM', 'fail':'TransferBracPT2SM'})
            smach.StateMachine.add('ActivateUR5FlowBSM', ActivateUR5FlowBSM(), transitions={'success':'TransferKDPT1SM'})
            smach.StateMachine.add('TransferKDPT1SM', TransferKDPT1SM(), transitions={'success':'TransferGPPT1SM', 'fail':'TransferKDPT1SM'})
            smach.StateMachine.add('TransferGPPT1SM', TransferGPPT1SM(), transitions={'success':'ActivateTipInspCSM_Rect', 'fail':'TransferGPPT1SM'})
            smach.StateMachine.add('ActivateTipInspCSM_Rect', ActivateTipInspCSM(), transitions={'success':'TransferRectIB1SM_1'})
            smach.StateMachine.add('TransferRectIB1SM_1', TransferRectIB1SM(), transitions={'success':'TransferRectIB1SM_2', 'fail':'TransferRectIB1SM_1'})
            smach.StateMachine.add('TransferRectIB1SM_2', TransferRectIB1SM(), transitions={'success':'TransferTPWBSM', 'fail':'TransferRectIB1SM_2'})
            smach.StateMachine.add('TransferTPWBSM', TransferTPWBSM(), transitions={'success':'ExtendDryBaySM', 'fail':'TransferTPWBSM'})
            smach.StateMachine.add('ExtendDryBaySM', ExtendDryBaySM(), transitions={'success':'TransferTrayDBSM'})
            smach.StateMachine.add('TransferTrayDBSM', TransferTrayDBSM(), transitions={'success':'RetractWetBaySM', 'fail':'TransferTrayDBSM'})
            smach.StateMachine.add('RetractWetBaySM', RetractWetBaySM(), transitions={'success':'TransferIndiDBSM'})
            smach.StateMachine.add('TransferIndiDBSM', TransferIndiDBSM(), transitions={'success':'WaitRect', 'fail':'TransferIndiDBSM'})
            smach.StateMachine.add('WaitRect', WaitRect(), transitions={'success':'TransferRectDBSM', 'fail':'WaitRect'})
            smach.StateMachine.add('TransferRectDBSM', TransferRectDBSM(), transitions={'success':'FaultyInst_Rect', 'fail':'TransferRectDBSM'})
            smach.StateMachine.add('FaultyInst_Rect', FaultyInst(), transitions={'success':'ActivateTipInspCSM_CJ', 'fail':'FaultyInst_Rect'})
            smach.StateMachine.add('ActivateTipInspCSM_CJ', ActivateTipInspCSM(), transitions={'success':'TransferCJIB1SM_1'})
            smach.StateMachine.add('TransferCJIB1SM_1', TransferCJIB1SM(), transitions={'success':'TransferCJIB1SM_2', 'fail':'TransferCJIB1SM_1'})
            smach.StateMachine.add('TransferCJIB1SM_2', TransferCJIB1SM(), transitions={'success':'TransferCJIB1SM_3', 'fail':'TransferCJIB1SM_2'})
            smach.StateMachine.add('TransferCJIB1SM_3', TransferCJIB1SM(), transitions={'success':'TransferCJIB1SM_4', 'fail':'TransferCJIB1SM_3'})
            smach.StateMachine.add('TransferCJIB1SM_4', TransferCJIB1SM(), transitions={'success':'TransferCJIB1SM_5', 'fail':'TransferCJIB1SM_4'})
            smach.StateMachine.add('TransferCJIB1SM_5', TransferCJIB1SM(), transitions={'success':'TransferCJIB1SM_6', 'fail':'TransferCJIB1SM_5'})
            smach.StateMachine.add('TransferCJIB1SM_6', TransferCJIB1SM(), transitions={'success':'FaultyInst_CJ', 'fail':'TransferCJIB1SM_6'})
            smach.StateMachine.add('FaultyInst_CJ', FaultyInst(), transitions={'success':'TransferGPDBSM', 'fail':'FaultyInst_CJ'})
            smach.StateMachine.add('TransferGPDBSM', TransferGPDBSM(), transitions={'success':'TransferKDDBSM', 'fail':'TransferGPDBSM'})
            smach.StateMachine.add('TransferKDDBSM', TransferKDDBSM(), transitions={'success':'ActivateTipInspCSM_LI', 'fail':'TransferKDDBSM'})
            smach.StateMachine.add('ActivateTipInspCSM_LI', ActivateTipInspCSM(), transitions={'success':'ActivateFlatInspDSM_LI'})
            smach.StateMachine.add('ActivateFlatInspDSM_LI', ActivateFlatInspDSM(), transitions={'success':'TransferLIIB1SM_1'})
            smach.StateMachine.add('TransferLIIB1SM_1', TransferLIIB1SM(), transitions={'success':'TransferLIIB1SM_2', 'fail':'TransferLIIB1SM_1'})
            smach.StateMachine.add('TransferLIIB1SM_2', TransferLIIB1SM(), transitions={'success':'TransferLIIB1SM_3', 'fail':'TransferLIIB1SM_2'})
            smach.StateMachine.add('TransferLIIB1SM_3', TransferLIIB1SM(), transitions={'success':'TransferLIIB1SM_4', 'fail':'TransferLIIB1SM_3'})
            smach.StateMachine.add('TransferLIIB1SM_4', TransferLIIB1SM(), transitions={'success':'TransferLIIB1SM_5', 'fail':'TransferLIIB1SM_4'})
            smach.StateMachine.add('TransferLIIB1SM_5', TransferLIIB1SM(), transitions={'success':'TransferLIIB1SM_6', 'fail':'TransferLIIB1SM_5'})
            smach.StateMachine.add('TransferLIIB1SM_6', TransferLIIB1SM(), transitions={'success':'DispenseMagilSM', 'fail':'TransferLIIB1SM_6'})
            smach.StateMachine.add('DispenseMagilSM', DispenseMagilSM(), transitions={'success':'FaultyInst_LI'})
            smach.StateMachine.add('FaultyInst_LI', FaultyInst(), transitions={'success':'WaitTempBracket', 'fail':'FaultyInst_LI'})
            smach.StateMachine.add('WaitTempBracket', WaitTempBracket(), transitions={'success':'TransferTBDBSM', 'fail':'WaitTempBracket'})
            smach.StateMachine.add('TransferTBDBSM', TransferTBDBSM(), transitions={'success':'WaitSecondBracket', 'fail':'TransferTBDBSM'})
            smach.StateMachine.add('WaitSecondBracket', WaitSecondBracket(), transitions={'success':'ActivatePBSTSM', 'fail':'WaitSecondBracket'})
            smach.StateMachine.add('ActivatePBSTSM', ActivatePBSTSM(), transitions={'success':'TransferSBDBSM'})
            smach.StateMachine.add('TransferSBDBSM', TransferSBDBSM(), transitions={'success':'TransferWPDBSM_1', 'fail':'TransferSBDBSM'})
            smach.StateMachine.add('TransferWPDBSM_1', TransferWPDBSM(), transitions={'success':'TransferWPDBSM_2', 'fail':'TransferWPDBSM_1'})
            smach.StateMachine.add('TransferWPDBSM_2', TransferWPDBSM(), transitions={'success':'TransferWPLDBSM', 'fail':'TransferWPDBSM_2'})
            smach.StateMachine.add('TransferWPLDBSM', TransferWPLDBSM(), transitions={'success':'TransferSTDBSM', 'fail':'TransferWPLDBSM'})
            smach.StateMachine.add('TransferSTDBSM', TransferSTDBSM(), transitions={'success':'RetractDryBaySM', 'fail':'TransferSTDBSM'})
            smach.StateMachine.add('RetractDryBaySM', RetractDryBaySM(), transitions={'success':'CheckAllSetProccessedSM'})
            smach.StateMachine.add('CheckAllSetProccessedSM', CheckAllSetProccessedSM(), transitions={'success':'success', 'fail':'ActivateAirKnifeSM'})
        smach.StateMachine.add('MainFlowASM', MainFlowASM, transitions={'success': 'ended'})
        
    smach_viewer = smach_ros.IntrospectionServer('bigbox_smach_server', sm, '/Start')
    smach_viewer.start()

    outcome = sm.execute()
    rospy.spin()
    smach_viewer.stop()

if __name__ == '__main__':
    main()
    # a = FaultyInst()
    # a.execute()