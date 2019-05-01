#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String

def talker():
    pub1 = rospy.Publisher('gazebo', String, queue_size=10)
    pub2 = rospy.Publisher('ekf', String, queue_size=10)
    rospy.init_node('infrared', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub1.publish(hello_str)
        pub2.publish(hello_str)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
