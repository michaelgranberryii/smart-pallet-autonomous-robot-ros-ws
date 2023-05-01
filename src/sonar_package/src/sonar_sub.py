#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32
import time #Delay
from geometry_msgs.msg import Twist



class Sub:
	def __init__(self):
		rospy.init_node('sonar_listener', anonymous=True)
		self.t70 = 'sonar70_range_topic'
		self.t72 = 'sonar72_range_topic'
		self.t74 = 'sonar74_range_topic'
		self.t75 = 'sonar75_range_topic'
		self.t77 = 'sonar77_range_topic'
		self.a =rospy.Subscriber(self.t70, Int32, self.sonar_callback_0x70)
		self.b =rospy.Subscriber(self.t72, Int32, self.sonar_callback_0x72)
		self.c =rospy.Subscriber(self.t74, Int32, self.sonar_callback_0x74)
		self.c =rospy.Subscriber(self.t75, Int32, self.sonar_callback_0x75)
		self.c =rospy.Subscriber(self.t77, Int32, self.sonar_callback_0x77)

		self.range_sonar_far_left = 25 #0x75
		self.range_sonar_left = 25 #0x74
		self.range_sonar_center = 25 #0x70
		self.range_sonar_right = 25 #0x72
		self.range_sonar_far_right = 25 #0x75

		# Sonar Array List
		self.sonar_list = []

		# Safe Distance
		self.safe_dist = 10
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

	def listener(self):
		rate = rospy.Rate(10)
		while not rospy.is_shutdown():
			rospy.loginfo("listener is called")
			self.obj_avoidance()
			rate.sleep()

	# def listener(self):
	# 	rospy.init_node('sonar_listener', anonymous=True)
	# 	rate = rospy.Rate(10)
	# 	while not rospy.is_shutdown():
			
	# 		rospy.Subscriber(self.t70, Int32, self.sonar_callback_0x70)
	# 		rospy.Subscriber(self.t72, Int32, self.sonar_callback_0x72)
	# 		rospy.Subscriber(self.t74, Int32, self.sonar_callback_0x74)
	# 		rospy.loginfo("LISTN")
	# 		self.obj_avoidance()
	# 		rate.sleep()
			# rospy.spin()

	def obj_avoidance(self):
		rospy.loginfo("sonar700: " + str(self.range_sonar_left))
		rospy.loginfo("sonar722: " + str(self.range_sonar_center))
		rospy.loginfo("sonar744: " + str(self.range_sonar_right))

		if self.range_sonar_left < 27:
			rospy.loginfo("turn_right is called")
			self.turn_right()

		# elif self.range_sonar_center < 27:
		# 	rospy.loginfo("center")

		elif self.range_sonar_right < 27:
			rospy.loginfo("turn_left is called")
			self.turn_left()

		else:
			rospy.loginfo("drive_foward is called")
			self.drive_forward()

	def stop(self):
		# Initialize the node and set the publisher topic
		# rospy.init_node('velocity_publisher', anonymous=True)
		pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

		# Set the rate of publishing to 10 Hz
		rate = rospy.Rate(10)

		# Create a Twist message to hold the velocity command
		velocity_cmd = Twist()
		velocity_cmd.angular.z = 0.1

		# Loop until the node is shut down
		# while not rospy.is_shutdown():
			# Publish the velocity command
		pub.publish(velocity_cmd)

		# Sleep to maintain the publishing rate
		rate.sleep()

	def turn_left(self):
		# Initialize the node and set the publisher topic
		# rospy.init_node('velocity_publisher', anonymous=True)
		pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

		# Set the rate of publishing to 10 Hz
		rate = rospy.Rate(10)

		# Create a Twist message to hold the velocity command
		velocity_cmd = Twist()
		velocity_cmd.angular.z = 0.8

		# Loop until the node is shut down
		# while not rospy.is_shutdown():
			# Publish the velocity command
		pub.publish(velocity_cmd)

		# Sleep to maintain the publishing rate
		rate.sleep()

	def turn_right(self):
		# Initialize the node and set the publisher topic
		# rospy.init_node('velocity_publisher', anonymous=True)
		pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

		# Set the rate of publishing to 10 Hz
		rate = rospy.Rate(10)

		# Create a Twist message to hold the velocity command
		velocity_cmd = Twist()
		velocity_cmd.angular.z = -0.8

		# Loop until the node is shut down
		# while not rospy.is_shutdown():
			# Publish the velocity command
		pub.publish(velocity_cmd)

		# Sleep to maintain the publishing rate
		rate.sleep()

	def drive_forward(self):
		# Initialize the node and set the publisher topic
		# rospy.init_node('velocity_publisher', anonymous=True)
		pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

		# Set the rate of publishing to 10 Hz
		rate = rospy.Rate(10)

		# Create a Twist message to hold the velocity command
		velocity_cmd = Twist()
		velocity_cmd.linear.x = 0.1 # set linear x velocity to 0.1 m/s

		# Loop until the node is shut down
		# while not rospy.is_shutdown():
			# Publish the velocity command
		pub.publish(velocity_cmd)

		# Sleep to maintain the publishing rate
		rate.sleep()

if __name__ == '__main__':
	subscriber = Sub()
	subscriber.listener()
	

