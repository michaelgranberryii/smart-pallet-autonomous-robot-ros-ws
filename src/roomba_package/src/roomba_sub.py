#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32
from std_msgs.msg import String
import time #Delay
from geometry_msgs.msg import Twist



class Sub:
	def __init__(self):
		rospy.init_node('sonar_listener', anonymous=True)
		self.ta = 'sonar70_range_topic'
		self.tb = 'sonar72_range_topic'
		self.tc = 'sonar74_range_topic'
		self.td = 'video_label'
		self.a =rospy.Subscriber(self.ta, Int32, self.sonar_callback_0x70)
		self.b =rospy.Subscriber(self.tb, Int32, self.sonar_callback_0x72)
		self.c =rospy.Subscriber(self.tc, Int32, self.sonar_callback_0x74)
		self.d =rospy.Subscriber(self.td, String, self.video_label_callback)

		self.range_sonar_left = 25 #0x70
		self.range_sonar_center = 25 #0x71
		self.range_sonar_right = 25 #0x72

		self.video_label = []

		# Sonar Array List
		self.sonar_list = []

		# Safe Distance
		self.safe_dist = 10
		self.min_range_reading = 0

	def sonar_callback_0x70(self, message):
		self.range_sonar_left = message.data
		# rospy.loginfo("sonar700: " + str(self.range_sonar_left))

	def sonar_callback_0x72(self, message):
		self.range_sonar_center = message.data
		# rospy.loginfo("sonar722: " + str(self.range_sonar_center))

	def sonar_callback_0x74(self, message):
		self.range_sonar_right = message.data
		# rospy.loginfo("sonar744: " + str(self.range_sonar_right))

	def video_label_callback(self, message):
		self.video_label = message.data
		rospy.loginfo("video label: " + self.video_label)

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
			
	# 		rospy.Subscriber(self.t1, Int32, self.sonar_callback_0x70)
	# 		rospy.Subscriber(self.t2, Int32, self.sonar_callback_0x72)
	# 		rospy.Subscriber(self.t3, Int32, self.sonar_callback_0x74)
	# 		rospy.loginfo("LISTN")
	# 		self.obj_avoidance()
	# 		rate.sleep()
			# rospy.spin()

	def obj_avoidance(self):
		rospy.loginfo("sonar700: " + str(self.range_sonar_left))
		rospy.loginfo("sonar722: " + str(self.range_sonar_center))
		rospy.loginfo("sonar744: " + str(self.range_sonar_right))
		rospy.loginfo("I see: " + str(self.video_label))

		if (self.range_sonar_left < 27) or (self.video_label == 'person'):
			rospy.loginfo("turn_right is called")
			rospy.loginfo("I see: " + str(self.video_label))
			self.turn_right()
		elif self.range_sonar_center < 27:
			rospy.loginfo("center")
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
		velocity_cmd.angular.z = 0.1

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
		velocity_cmd.angular.z = -0.1

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
	

