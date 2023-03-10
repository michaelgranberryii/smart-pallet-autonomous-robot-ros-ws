#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32
from sensor_msgs.msg import Range

class ObstDet():
	def __init__(self):
		rospy.init_node('sonar_listener_algo', anonymous=True)
		self.range_sonar_left = 25
		self.range_sonar_center = 25 
		self.range_sonar_right = 25
		
		self.sub_sonar0x70 = rospy.Subscriber("sonar0x70_range_topic", Int32, self.update_range0x70)
		self.sub_sonar0x72 = rospy.Subscriber("sonar0x72_range_topic", Int32, self.update_range0x72)
		self.sub_sonar0x74 = rospy.Subscriber("sonar0x74_range_topic", Int32, self.update_range0x74)
		rospy.loginfo("Subscribers set")
		
	def update_range0x70(self, message):
	 	self.range_sonar_left = message.data
	 	#rospy.loginfo("sonar0x70: " + str(message.data))
	 	#rospy.loginfo(str(self.range_sonar0x70))
	 	
	def update_range0x72(self, message):
	 	self.range_sonar_center = message.data
	 	#rospy.loginfo("sonar0x72: " + str(message.data))
	 	#rospy.loginfo(str(self.range_sonar0x72))
	 
	def update_range0x74(self, message):
	 	self.range_sonar_right = message.data
	 	#rospy.loginfo("sonar0x74: " + str(message.data))
	 	#rospy.loginfo(str(self.range_sonar0x74))

	def run(self):
		rate = rospy.Rate(10)
		while not rospy.is_shutdown():
			self.boolFun()
			rate.sleep() 
			
	def boolFun(self):
		if (self.range_sonar_center < 100):
			rospy.loginfo("Stop and turn 180!")
		elif (self.range_sonar_left < 100):
			rospy.loginfo("Stop and turn right!")
		elif (self.range_sonar_left < 100) and (self.range_sonar_center < 100):
			rospy.loginfo("Stop and turn right! : LC")
		elif (self.range_sonar_right < 100):
			rospy.loginfo("Stop and turn left!")
		elif (self.range_sonar_right < 100) and (self.range_sonar_center < 100):
			rospy.loginfo("Stop and turn left! : RC")
		elif (self.range_sonar_left < 100) and (self.range_sonar_center < 100) and (self.range_sonar_right < 100):
			rospy.loginfo("Stop!")
		else:
			rospy.loginfo("Drive!")
		

if __name__ == '__main__':
	
	obst_det = ObstDet()
	obst_det.run()
	
	
