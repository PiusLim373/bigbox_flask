#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from flask import jsonify

def talker():
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    # rate = rospy.Rate(10) # 10hz
    data = "hi"
    # hello_str = jsonify(data)
    print(data)
    rospy.loginfo(data)
    pub.publish(str(data))
    # rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
