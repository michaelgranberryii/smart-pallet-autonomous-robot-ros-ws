#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int32
from sensor_msgs.msg import Range
import time #Delay

class ObstDet():
	def __init__(self):
		rospy.init_node('sonar_listener_algo', anonymous=True)

		# Sonar Vars
		self.range_sonar_left = 25 #0x70
		self.range_sonar_center = 25 #0x72
		self.range_sonar_right = 25 #0x74

		# Sonar Array List
		self.sonar_list = []

		# Sonar Array indecies
		self.l=0
		self.c=1
		self.r=2

		# Safe Distance
		self.safe_dist = 100
		
		# Sonar Subscribers
		self.sub_sonar0x70 = rospy.Subscriber('sonar0x70_range_topic', Int32, self.update_range0x70)
		self.sub_sonar0x72 = rospy.Subscriber('sonar0x72_range_topic', Int32, self.update_range0x72)
		self.sub_sonar0x74 = rospy.Subscriber('sonar0x74_range_topic', Int32, self.update_range0x74)
		rospy.loginfo("Subscribers set")
		
	def update_range0x70(self, message):
		self.range_sonar_left = message.data
		# rospy.loginfo(str(message.data))

	def update_range0x72(self, message):
		self.range_sonar_center = message.data
		# rospy.loginfo(str(message.data))
	 
	def update_range0x74(self, message):
		self.range_sonar_right = message.data
		# rospy.loginfo(str(message.data))

	def get_sonar_list(self):
		self.s_list = [self.range_sonar_left, self.range_sonar_center, self.range_sonar_right]
		return self.s_list
			
	def boolFun(self):
		self.sonar_list = self.get_sonar_list()
		rospy.loginfo(self.sonar_list)

		for index, r in enumerate(self.sonar_list):
			if r < self.safe_dist:
				rospy.loginfo("Hover")
				if index == 0:
					while (r < self.safe_dist):
						time.sleep(.5)
						rospy.loginfo(self.sonar_list)
						rospy.loginfo("Rotate Right")
						r = self.range_sonar_left

				elif index == 1:
					while ([self.range_sonar_left, self.range_sonar_center, self.range_sonar_right] > [self.safe_dist, self.safe_dist, self.safe_dist]):
						time.sleep(.5)
						rospy.loginfo(self.sonar_list)
						rospy.loginfo("Hover: 1")
						
						max_dis = max(self.sonar_list[self.l], self.sonar_list[self.r])
						if (max_dis == self.sonar_list[self.l]):
							rospy.loginfo("H: Rotate Left")
						else:
							rospy.loginfo("H: Rotate Right")
						

				elif index == 2:
					while (r < self.safe_dist):
						time.sleep(.5)
						rospy.loginfo(self.sonar_list)
						rospy.loginfo("Rotate Left")
						r = self.range_sonar_right

				else:
					rospy.loginfo(self.sonar_list)
					rospy.loginfo("Hover")

			rospy.loginfo(self.sonar_list)
			rospy.loginfo("Drive")

		
	def run(self):
		rate = rospy.Rate(3)
		while not rospy.is_shutdown():
			self.boolFun()
			rate.sleep()
			
if __name__ == '__main__':
	
	obst_det = ObstDet()
	obst_det.run()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
