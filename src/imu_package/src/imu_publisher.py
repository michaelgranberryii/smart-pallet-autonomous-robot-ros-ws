#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32
from sensor_msgs.msg import Range
import imu_package.bimu as imu
import time #Delay


def imu_talker():
	pub = rospy.Publisher('imu_topic', Float32, queue_size=10) # publisher object
	rospy.init_node('imu_publisher_node', anonymous=True) # initialize publisher node
	rate = rospy.Rate(100) # ros rate
	rospy.loginfo("ROS imu node now publishing.")
	bimu = imu.BIMU()
	bimu.detect_imu_connection()
	while not rospy.is_shutdown():
		bimu.read()
		rangeValue = bimu.getgyroXangle()
		rospy.loginfo(rangeValue)
		pub.publish(rangeValue)
		rate.sleep()

if __name__ == "__main__":
	try:
		imu_talker()
	except rospy.ROSInterruptException:
		pass
		
		
		




