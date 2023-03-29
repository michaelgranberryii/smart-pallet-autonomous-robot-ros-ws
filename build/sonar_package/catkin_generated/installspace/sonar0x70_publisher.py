#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int32
from sensor_msgs.msg import Range
import sonar_package.sonar as sp
import time #Delay


def sonar_talker():
	pub = rospy.Publisher('sonar0x70_range_topic', Int32, queue_size=10) # publisher object
	rospy.init_node('sonar0x70_publisher_node', anonymous=True) # initialize publisher node
	rate = rospy.Rate(10) # ros rate
	rospy.loginfo("Ros sonar node now publishing.")
	s = sp.Sonar(0x70)
	while not rospy.is_shutdown():
		rangeValue = s.read_range()
		rospy.loginfo(rangeValue)
		pub.publish(rangeValue)
		rate.sleep()

if __name__ == "__main__":
	try:
		sonar_talker()
	except rospy.ROSInterruptException:
		pass
		
		
		




