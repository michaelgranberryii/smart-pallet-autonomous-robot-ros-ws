import cv2 as cv

classification = []
classFile = "/home/ubuntu/Object_Detection_Files/coco.names"
with open(classFile,"rt") as p:
    classification = p.read().rstrip("\n").split("\n")
configPath = "/home/ubuntu/Object_Detection_Files/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weights = "/home/ubuntu/Object_Detection_Files/frozen_inference_graph.pb"

net = cv.dnn_DetectionModel(weights,configPath)
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
                    cv.rectangle(img,box,color = (0,255,0), thickness =2)
                    cv.putText(img, classification[classId-1].upper(),(box[0],box[1]), cv.FONT_HERSHEY_COMPLEX, 1, (0,255,0),2)
                    cv.putText(img,str(round(confidence*100,2)),(box[1], box[0]), cv.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
    return img, objectInfo
if __name__ == "__main__":
    cap = cv.VideoCapture(0)
    cap.set(3,480)
    cap.set(4,480)

    while True:
        success, img = cap.read()
        result, objectInfo = getObject(img,0.65,0.1, objects = ['person','phone'])
        cv.imshow("ObjectDetection",img)
        cv.waitKey(1)


