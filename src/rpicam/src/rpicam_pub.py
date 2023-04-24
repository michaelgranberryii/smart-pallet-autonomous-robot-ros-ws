#!/usr/bin/env python3
import rpicam.ObjectDetection as rpi
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2



def publish_message():
    pub = rospy.Publisher('video_frames', Image, queue_size=10)
    rospy.init_node('video_pub_py', anonymous=True)
    rate = rospy.Rate(60)

    camera = rpi.Cam()
    

    br = CvBridge()

    while not rospy.is_shutdown():
        ret, frame = camera.read_cap()
        result, objectInfo = camera.getObject(frame, 0.45, 0.2, objects = ['person','phone'])
        cv2.imshow("rpicam/ObjectDetection",frame)
        cv2.waitKey(1)
        if ret == True:
            rospy.loginfo('publishing video frame')
            pub.publish(br.cv2_to_imgmsg(frame))
        rate.sleep()

if __name__ == '__main__':
    try:
        publish_message()
    except rospy.ROSInterruptException:
        pass
