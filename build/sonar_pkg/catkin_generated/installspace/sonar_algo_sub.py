#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int32
from sensor_msgs.msg import Range

class ObstDet():
	def __init__(self):
		rospy.init_node('sonar_listener_algo', anonymous=True)
		self.range_sonar0x70 = 25
		self.range_sonar0x72 = 25
		self.range_sonar0x74 = 25
		
		self.sub_sonar0x70 = rospy.Subscriber("sonar0x70_range_topic", Int32, self.update_range0x70)
		self.sub_sonar0x72 = rospy.Subscriber("sonar0x72_range_topic", Int32, self.update_range0x72)
		self.sub_sonar0x74 = rospy.Subscriber("sonar0x74_range_topic", Int32, self.update_range0x74)
		rospy.loginfo("Subscribers set")
		
	def update_range0x70(self, message):
	 	self.range_sonar0x70 = message.data
	 	#rospy.loginfo("sonar0x70: " + str(message.data))
	 	#rospy.loginfo(str(self.range_sonar0x70))
	 	
	def update_range0x72(self, message):
	 	self.range_sonar0x72 = message.data
	 	#rospy.loginfo("sonar0x72: " + str(message.data))
	 	#rospy.loginfo(str(self.range_sonar0x72))
	 
	def update_range0x74(self, message):
	 	self.range_sonar0x74 = message.data
	 	#rospy.loginfo("sonar0x74: " + str(message.data))
	 	#rospy.loginfo(str(self.range_sonar0x74))

	def run(self):
		rate = rospy.Rate(5)
		while not rospy.is_shutdown():
			self.boolFun()
			rate.sleep() 
			
	def boolFun(self):
		if (self.range_sonar0x70 < 100) or (self.range_sonar0x72 < 100) or (self.range_sonar0x70 < 100):
			rospy.loginfo("Range is 100 cm or less")
		else:
			rospy.loginfo("Range is greater than 100 cm")
		

if __name__ == '__main__':
	
	obst_det = ObstDet()
	obst_det.run()
	
	
