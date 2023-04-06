#!/usr/bin/env python3
import rospy
import cvlib as cv
from cvlib.object_detection import draw_bbox
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

cap = cv2.VideoCapture(0)

def publish_message():
    pub = rospy.Publisher('video_frames', Image, queue_size=10)
    rospy.init_node('video_pub_py', anonymous=True)

    rate = rospy.Rate(60)


    br = CvBridge()

    while not rospy.is_shutdown():

        ret, frame = cap.read()
        bbox, label, conf = cv.detect_common_objects(frame) #added by Gavin
        out_img = draw_bbox(frame, bbox, label, conf) #added with love by gavin
        if ret == True:
            rospy.loginfo('publishing video frame')

            pub.publish(br.cv2_to_imgmsg(frame))
            #cv2.imshow("Object_Detection", out_img) #added by gavin
        rate.sleep()

if __name__ == '__main__':
    try:
        publish_message()
    except rospy.ROSInterruptException:
        pass
