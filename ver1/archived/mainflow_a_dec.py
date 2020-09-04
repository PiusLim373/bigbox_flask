#!/usr/bin/env python
import smach
import smach_ros
import rospy
from smach import CBState
from time import sleep
from main import ErrorRecovery
        

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
        sleep(2)
        if self.success:
            rospy.loginfo("Transfer completed")
            return 'success'
        else:
            self.success = ErrorRecovery(self.success)
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

class FaultyInst(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success', 'fail'])

    def execute(self, userdata):
        rospy.loginfo("Check for faulty instrument...")
        #connect to sql IB database to check for any faulty instruments to be replenished 
        #faulty_instruments = connectsql...
        #
        faulty_instruments = ['retractor', 'retractor']
        sleep(2)
        while len(faulty_instruments) != 0:
            rospy.logwarn("Faulty instument detected by Inspection Bay, list: " + faulty_instruments)
            rospy.logwarn("Proceeding to replace faulty instrument...")
            for x in faulty_instruments:
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
                    faulty_instruments.remove(x)
        #clear list from sql
        #
        return 'success'







class CheckAllSetProccessedSM(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success', 'fail'], input_keys=['pigeonhole_to_process','pigeonhole_processing'], output_keys=['pigeonhole_processing'])
        self.counter = 1

    def execute(self, userdata):
        rospy.loginfo("Pigeon hole no: " + str(userdata.pigeonhole_processing) + " process completed successfully")
        if self.counter < len(userdata.pigeonhole_to_process):
            userdata.pigeonhole_processing = userdata.pigeonhole_to_process[self.counter]
            rospy.loginfo("Next pigeon hole to process: " + str(userdata.pigeonhole_processing) )
            self.counter += 1
            return 'fail'
        else:
            rospy.loginfo("All pigeon hole has been processed!")
            return 'success'

