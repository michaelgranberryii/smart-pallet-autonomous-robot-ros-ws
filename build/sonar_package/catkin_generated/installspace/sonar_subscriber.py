#----------------------------------------
#Engineer: Michael Granberry
#Project: ARCS Smart Pallet
#Device: Ultrasonic Sensor
#Model: I2C MaxSonar EZ Series - MB1212
#Program: ROS Subscriber Node
#Last Modified Date: Oct 23, 2022
#----------------------------------------

#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32

def sonar_callback_0x70(message):
	rospy.loginfo("sonar0x70: " + str(message.data))

def sonar_callback_0x72(message):
	rospy.loginfo("sonar0x72: " + str(message.data))

def sonar_callback_0x74(message):
	rospy.loginfo("sonar0x74: " + str(message.data))

def listener():
	rospy.init_node('sonar_listener', anonymous=True)
	rospy.Subscriber("sonar0x70_range_topic", Int32, sonar_callback_0x70)
	rospy.Subscriber("sonar0x72_range_topic", Int32, sonar_callback_0x72)
	rospy.Subscriber("sonar0x74_range_topic", Int32, sonar_callback_0x74)
	rospy.spin()

if __name__ == '__main__':
	listener()
	
