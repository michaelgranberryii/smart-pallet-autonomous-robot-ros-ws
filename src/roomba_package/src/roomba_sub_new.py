#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32
from std_msgs.msg import String
import time #Delay
from geometry_msgs.msg import Twist



class Sub:
	def __init__(self):
		rospy.init_node('sonar_listener_2', anonymous=True)
		self.t_70 = 'sonar70_range_topic'
		self.t_72 = 'sonar72_range_topic'
		self.t_74 = 'sonar74_range_topic'
		self.t_75 = 'sonar75_range_topic'
		self.t_77 = 'sonar77_range_topic'
		self.t_videocam = 'video_label'
		self.t_thermalcam = 'thermal_video_label'

		self.a =rospy.Subscriber(self.t_70, Int32, self.sonar_callback_0x70)
		self.b =rospy.Subscriber(self.t_72, Int32, self.sonar_callback_0x72)
		self.c =rospy.Subscriber(self.t_74, Int32, self.sonar_callback_0x74)
		self.c =rospy.Subscriber(self.t_75, Int32, self.sonar_callback_0x75)
		self.c =rospy.Subscriber(self.t_77, Int32, self.sonar_callback_0x77)
		self.d =rospy.Subscriber(self.t_videocam, String, self.video_label_callback)
		self.e =rospy.Subscriber(self.t_thermalcam, String, self.thermal_video_label_callback)

		self.range_sonar_far_left = 25 #0x75
		self.range_sonar_left = 25 #0x74
		self.range_sonar_center = 25 #0x70
		self.range_sonar_right = 25 #0x72
		self.range_sonar_far_right = 25 #0x77

		self.video_label = ''
		self.thermal_video_label = ''

		# Sonar Array List
		self.sonar_list = []

		# Safe Distance
		self.safe_dist = 30
		self.min_range_reading = 0

	def sonar_callback_0x75(self, message):
		self.range_sonar_far_left = message.data
		# rospy.loginfo("sonar744: " + str(self.range_sonar_far_left))

	def sonar_callback_0x74(self, message):
		self.range_sonar_left = message.data
		# rospy.loginfo("sonar700: " + str(self.range_sonar_left))

	def sonar_callback_0x70(self, message):
		self.range_sonar_center = message.data
		# rospy.loginfo("sonar722: " + str(self.range_sonar_center))

	def sonar_callback_0x72(self, message):
		self.range_sonar_right = message.data
		# rospy.loginfo("sonar744: " + str(self.range_sonar_right))

	def sonar_callback_0x77(self, message):
		self.range_sonar_far_right = message.data
		# rospy.loginfo("sonar744: " + str(self.range_sonar_far_right))

	def video_label_callback(self, message):
		self.video_label = message.data
		rospy.loginfo("video label: " + self.video_label)

	def thermal_video_label_callback(self, message):
		self.thermal_video_label = message.data
		rospy.loginfo("video label: " + self.thermal_video_label)

	def listener(self):
		rate = rospy.Rate(10)
		while not rospy.is_shutdown():
			rospy.loginfo("listener is called")
			self.obj_avoidance()
			rate.sleep()

	def sonar_list(self):
		self.sonar_list = [self.range_sonar_far_left, self.range_sonar_left, self.range_sonar_center, self.range_sonars_right, self.range_sonar_far_right]
		
	def obj_avoidance(self):
		# rospy.loginfo("sonar77: " + str(self.range_sonar_far_right))
		# rospy.loginfo("sonar72: " + str(self.range_sonar_right))
		# rospy.loginfo("sonar70: " + str(self.range_sonar_center))
		# rospy.loginfo("sonar74: " + str(self.range_sonar_left))
		# rospy.loginfo("sonar75: " + str(self.range_sonar_far_left))
		rospy.loginfo('77: ' + str(self.range_sonar_far_right) + ', ' + '		72: ' + str(self.range_sonar_right) + ', ' + '		70: ' + str(self.range_sonar_center) + ', ' + '		74: ' + str(self.range_sonar_left) + ', ' + '		75: ' + str(self.range_sonar_far_left))


		if (self.video_label != ""):
			rospy.loginfo("Video camera sees: " + str(self.video_label))

		if (self.thermal_video_label != ""):
			rospy.loginfo("Thermal camera sees: " + str(self.thermal_video_label))



		# Main Algo
		if ((self.range_sonar_far_left > self.safe_dist) and (self.range_sonar_left > self.safe_dist) and (self.range_sonar_center > self.safe_dist) and (self.range_sonar_right > self.safe_dist) and (self.range_sonar_far_right > self.safe_dist)):
			rospy.loginfo("Drive is called")
			self.drive_forward()
		elif((self.range_sonar_far_left < self.safe_dist) or (self.range_sonar_left < self.safe_dist) or(self.range_sonar_center < self.safe_dist) or (self.range_sonar_right < self.safe_dist) or (self.range_sonar_far_right < self.safe_dist)):
			if(self.range_sonar_center < self.safe_dist):
				max_dist = max(self.range_sonar_far_left, self.range_sonar_left, self.range_sonar_right, self.range_sonar_far_right)
				if((max_dist == self.range_sonar_far_left) or (max_dist == self.range_sonar_left)):
					rospy.loginfo("Turn left_c is called")
					self.turn_left
				else:
					rospy.loginfo("Turn right_c is called")
					self.turn_right
			elif(self.range_sonar_far_left < self.safe_dist):
				rospy.loginfo("Turn right0 is called")
				self.turn_right()
			elif(self.range_sonar_left < self.safe_dist):
				rospy.loginfo("Turn right1 is called")
				self.turn_right()
			elif(self.range_sonar_right < self.safe_dist):
				rospy.loginfo("Turn left0 is called")
				self.turn_left()
			elif(self.range_sonar_far_right < self.safe_dist):
				rospy.loginfo("Turn left1 is called")
				self.turn_left()
			else:
				self.stop()
		else:
			self.stop()
			

	def stop(self):
		# Initialize the node and set the publisher topic
		pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

		# Set the rate of publishing to 10 Hz
		rate = rospy.Rate(10)

		# Create a Twist message to hold the velocity command
		velocity_cmd = Twist()
		velocity_cmd.linear.x = 0.0
		velocity_cmd.linear.y = 0.0
		velocity_cmd.linear.z = 0.0
		velocity_cmd.angular.x = 0.0
		velocity_cmd.angular.y = 0.0
		velocity_cmd.angular.z = 0.0

		# Publish the velocity command
		pub.publish(velocity_cmd)

		# Sleep to maintain the publishing rate
		rate.sleep()

	def turn_left(self):
		# Initialize the node and set the publisher topic
		pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

		# Set the rate of publishing to 10 Hz
		rate = rospy.Rate(10)

		# Create a Twist message to hold the velocity command
		velocity_cmd = Twist()
		velocity_cmd.angular.z = 0.1

		# Publish the velocity command
		pub.publish(velocity_cmd)

		# Sleep to maintain the publishing rate
		rate.sleep()

	def turn_right(self):
		# Initialize the node and set the publisher topic
		pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

		# Set the rate of publishing to 10 Hz
		rate = rospy.Rate(10)

		# Create a Twist message to hold the velocity command
		velocity_cmd = Twist()
		velocity_cmd.angular.z = -0.1

		# Publish the velocity command
		pub.publish(velocity_cmd)

		# Sleep to maintain the publishing rate
		rate.sleep()

	def drive_forward(self):
		# Initialize the node and set the publisher topic
		pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

		# Set the rate of publishing to 10 Hz
		rate = rospy.Rate(10)

		# Create a Twist message to hold the velocity command
		velocity_cmd = Twist()
		velocity_cmd.linear.x = 0.2 # set linear x velocity to 0.1 m/s

		# Publish the velocity command
		pub.publish(velocity_cmd)

		# Sleep to maintain the publishing rate
		rate.sleep()

if __name__ == '__main__':
	subscriber = Sub()
	subscriber.listener()
	

