#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int32
from sensor_msgs.msg import Range

class ObstDet():
	def __init__(self):
		rospy.init_node('sonar_listener_algo', anonymous=True)
		self.range_sonar_left = 25 #0x70
		self.range_sonar_center = 25 #0x72
		self.range_sonar_right = 25 #0x74
		self.l=0
		self.c=1
		self.r=2
		self.sonar_list = []
		self.max_dist = 254
		
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
	def turnLeft(self):
		rospy.loginfo("Stop and turn left! : RC")
		
	def turnRIght(self):
		rospy.loginfo("Stop and turn left! : RC")
		
	def turn180(self):
		rospy.loginfo("Stop and turn 180!")
		
	def get_sonar_list(self):
		self.slist = [self.range_sonar_left, self.range_sonar_center, self.range_sonar_right]
		return self.slist
			
	def boolFun(self):
		self.sonar_list = self.get_sonar_list()
		rospy.loginfo("L: " + str(self.sonar_list[self.l]) + " " + "C: " + str(self.sonar_list[self.c]) + " " + "R: " + str(self.sonar_list[self.r]))
		
		#if (self.sonar_list[self.c] < 100):
		#	rospy.loginfo("hover")
			
		#	if (self.sonar_list[self.r] == self.max_dist) and (self.sonar_list[self.l] < self.max_dist):
		#		rospy.loginfo("1turn right! : RC")
				
		#	elif (self.sonar_list[self.l] == self.max_dist) and (self.sonar_list[self.r] < self.max_dist):
		#		rospy.loginfo("2turn left! : RC")
				
		#else:
		#	rospy.loginfo("3turn left! : RC")
		
		if (self.sonar_list[self.c] < 100) or (self.sonar_list[self.r] < 100) or (self.sonar_list[self.l] < 100) :
			rospy.loginfo("hover")
			if (self.sonar_list[self.r] < 100):
				rospy.loginfo("rotate left")

		else:
			rospy.loginfo("drive")
			
if __name__ == '__main__':
	
	obst_det = ObstDet()
	obst_det.run()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
