#!/usr/bin/env python
import rospy
from std_msgs.msg import String

def callback(data):
    try:
        received_dict = eval(data.data)
        rospy.loginfo(received_dict['task'])
        if received_dict['task'] == "recheck":
            print('hi')
        else:
            print("boo")
    except:
        print("data received is not a dict")
    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)
    # rate = rospy.Rate(5)
    while not rospy.is_shutdown():
        rospy.Subscriber("chatter", String, callback)
        # print("hmm")
        # spin() simply keeps python from exiting until this node is stopped
        
        # rate.sleep()
        rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass