#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

cap = cv2.VideoCapture(0)
classification = []
classFile = "/home/ubuntu/Object_Detection_Files/coco.names"
with open(classFile,"rt") as p:
    classification = p.read().rstrip("\n").split("\n")
configPath = "/home/ubuntu/Object_Detection_Files/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weights = "/home/ubuntu/Object_Detection_Files/frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weights,configPath)
net.setInputSize(480,480)
net.setInputScale(1.0/127.5)
net.setInputMean((127.5,127.5,127.5))
net.setInputSwapRB(True)
def getObject(img,thres,nms,draw=True,objects = []):
    classIds, confs, bbox = net.detect(img,confThreshold = thres, nmsThreshold = nms)

    if len(objects) == 0: objects = classification
    objectInfo = []
    if len(classIds) != 0:
        for classId, confidence, box, in zip(classIds.flatten(),confs.flatten(),bbox):
            className = classification[classId - 1]
            if className in objects:
                objectInfo.append([box,className])
                if (draw):
                    cv2.rectangle(img,box,color = (0,255,0), thickness =2)
                    cv2.putText(img, classification[classId-1].upper(),(box[0],box[1]), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0),2)
                    cv2.putText(img,str(round(confidence*100,2)),(box[1], box[0]), cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
    return img, objectInfo

def publish_message():
    pub = rospy.Publisher('video_frames', Image, queue_size=10)
    rospy.init_node('video_pub_py', anonymous=True)

    rate = rospy.Rate(60)


    br = CvBridge()

    while not rospy.is_shutdown():

        ret, frame = cap.read()
        
        if ret == True:
            rospy.loginfo('publishing video frame')
            pub.publish(br.cv2_to_imgmsg(frame))
        rate.sleep()

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    cap.set(3,480)
    cap.set(4,480)
    try:
        publish_message()
    except rospy.ROSInterruptException:
        pass
