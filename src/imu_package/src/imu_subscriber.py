#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32
from sensor_msgs.msg import Range
import time #Delay

class ImuSub():
    def __init__(self):
        rospy.init_node('imu_listener', anonymous=True)
        self.gyroXangle = 0

        self.sub_gyroXangle = rospy.Subscriber('imu_topic', Float32, self.update_gyroXangle)


    def update_gyroXangle(self, message):
        self.gyroXangle = message.data
        rospy.loginfo(str(message.data))

    def getgyroXangle(self):
         rospy.loginfo(self.gyroXangle)

    def run(self):
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            self.getgyroXangle()
            rate.sleep()
                        
if __name__ == '__main__':
	
	obst_det = ImuSub()
	obst_det.run()