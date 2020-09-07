#!/usr/bin/env python
import rospy
from std_msgs.msg import String

def talker():
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    data = {'task': 'recheck'}
    rospy.loginfo(data)
    pub.publish(str(data))

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
