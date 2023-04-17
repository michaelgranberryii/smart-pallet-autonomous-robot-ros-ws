#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32
from sensor_msgs.msg import Range
import time #Delay

class ObstDet():
	def __init__(self):
		rospy.init_node('sonar_listener_algo', anonymous=True)

		# Sonar Vars
		self.range_sonar_left = 25 #0x70
		self.range_sonar_center = 25 #0x71
		self.range_sonar_right = 25 #0x72

		# Sonar Array List
		self.sonar_list = []

		# Sonar Array indecies
		self.l=0
		self.c=1
		self.r=2

		# Safe Distance
		self.safe_dist = 40
		self.min_range_reading = 0;
		
		# Sonar Subscribers
		self.sub_sonar0x70 = rospy.Subscriber('sonar0x70_range_topic', Int32, self.update_range0x70)
		self.sub_sonar0x72 = rospy.Subscriber('sonar0x71_range_topic', Int32, self.update_range0x71)
		self.sub_sonar0x74 = rospy.Subscriber('sonar0x72_range_topic', Int32, self.update_range0x72)
		rospy.loginfo("Subscribers set")
		
	def update_range0x70(self, message):
		self.range_sonar_left = message.data
		# rospy.loginfo(str(message.data))

	def update_range0x71(self, message):
		self.range_sonar_center = message.data
		# rospy.loginfo(str(message.data))
	 
	def update_range0x72(self, message):
		self.range_sonar_right = message.data
		# rospy.loginfo(str(message.data))

	def get_sonar_list(self):
		self.s_list = [self.range_sonar_left, self.range_sonar_center, self.range_sonar_right]
		return self.s_list
	
	def rotate_left(self):
		while (self.range_sonar_right < self.safe_dist):
			rospy.loginfo("Hover and Rotate Left")
			rospy.loginfo("Right: " + str(self.range_sonar_right) + "\n")

	
	def rotate_right(self):
		while (self.range_sonar_left < self.safe_dist):
			rospy.loginfo("Hover and Rotate Right")
			rospy.loginfo("Left: " + str(self.range_sonar_left) + "\n")

	
	def rotate_left_c(self):
		while ((self.range_sonar_right < self.safe_dist) and (self.range_sonar_center < self.safe_dist)):
			rospy.loginfo("Hover and Rotate Left_c")
			rospy.loginfo("Right: " + str(self.range_sonar_right) + "\n")

	
	def rotate_right_c(self):
		while ((self.range_sonar_left < self.safe_dist) and (self.range_sonar_center < self.safe_dist)):
			rospy.loginfo("Hover and Rotate Right_c")
			rospy.loginfo("Left: " + str(self.range_sonar_left) + "\n")

	def obj_avoidance(self):
		self.sonar_list = self.get_sonar_list()
		rospy.loginfo(self.sonar_list)

		if ((self.range_sonar_left < self.safe_dist) or (self.range_sonar_center < self.safe_dist) or (self.range_sonar_right < self.safe_dist)):
			rospy.loginfo("Hover")

			for index, r in enumerate(self.sonar_list):
				rospy.loginfo("index: " + str(index))
				rospy.loginfo("range: " + str(r))
				if (r < self.safe_dist):
					self.min_range_reading = r
					rospy.loginfo("min_range_reading: " + str(self.min_range_reading))

			if self.min_range_reading == self.range_sonar_center:
				max_range = max(self.range_sonar_left, self.range_sonar_right)
				rospy.loginfo("max: " + str(max_range))
				rospy.loginfo("C Left: " + str(self.range_sonar_left))
				rospy.loginfo("C Right: " + str(self.range_sonar_right))
				if (max_range == self.range_sonar_left):
					rospy.loginfo("Center L")
					self.rotate_left_c()
				else:
					rospy.loginfo("Center R")
					self.rotate_right_c()
				rospy.loginfo("\n")

			elif self.min_range_reading == self.range_sonar_left:
				self.rotate_right()
					

			elif self.min_range_reading == self.range_sonar_right: 
				self.rotate_left()

			else:
				rospy.loginfo("Hover\n")

		else:
			rospy.loginfo("Drive\n")
		
	def run(self):
		rate = rospy.Rate(10)
		while not rospy.is_shutdown():
			self.obj_avoidance()
			rate.sleep()
			
if __name__ == '__main__':
	
	obst_det = ObstDet()
	obst_det.run()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
