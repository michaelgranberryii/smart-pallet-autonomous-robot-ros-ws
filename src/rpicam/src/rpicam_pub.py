#!/usr/bin/env python3
import rpicam.ObjectDetection as rpi
import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
import cv2

camera = rpi.Cam()

def publish_message():
    pub = rospy.Publisher('video_frames', Image, queue_size=10)
    pub2 = rospy.Publisher('video_label', String, queue_size=10)
    rospy.init_node('video_pub_py', anonymous=True)
    rate = rospy.Rate(60)

    
    

    br = CvBridge()

    while not rospy.is_shutdown():
        ret, frame = camera.read_cap()
        result, objectInfo = camera.getObject(frame, 0.45, 0.2, objects = ['person','cup'])
        cv2.imshow("rpicam/ObjectDetection",frame)
        cv2.waitKey(1)
        label = ''

        # Label code
        if objectInfo == []:
            print("I found nothing")
        else:
            print("I found something")
            print(objectInfo[0])
            print(objectInfo[0][1])
            label = objectInfo[0][1]        
        # End label code


        if ret == True:
            rospy.loginfo('publishing video frame')
            pub.publish(br.cv2_to_imgmsg(frame))
            pub2.publish(label)
        rate.sleep()

if __name__ == '__main__':
    try:
        publish_message()
    except rospy.ROSInterruptException:
        pass
