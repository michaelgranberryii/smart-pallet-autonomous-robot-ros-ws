import cv2 as cv
import os




class Cam():
    def __init__(self):
        self.cap = cv.VideoCapture()
        self.cap.open("/dev/v4l/by-id/usb-GroupGets_PureThermal__fw:v1.3.0__8019001c-5111-3039-3433-373300000000-video-index0", cv.CAP_V4L)
        self.classification = []

        basePath = os.path.abspath(os.path.dirname(__file__))
        classFile = os.path.join(basePath, "dependencies/coco.names")
        with open(classFile,"rt") as p:
            self.classification = p.read().rstrip("\n").split("\n")


        modelFile = os.path.join(basePath, "dependencies/frozen_inference_graph.pb")
        configFile = os.path.join(basePath, "dependencies/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
        self.net = cv.dnn_DetectionModel(modelFile, configFile)

        self.net.setInputSize(480,480)
        self.net.setInputScale(1.0/127.5)
        self.net.setInputMean((127.5,127.5,127.5))
        self.net.setInputSwapRB(True)


        self.label = ''

    def setCap(self,cap):
        self.cap = cap

    def read_cap(self):
        ret, frame = self.cap.read()
        return ret, frame
    
    def getObject(self,img,thres,nms,draw=True,objects = []):
        classIds, confs, bbox = self.net.detect(img,confThreshold = thres, nmsThreshold = nms)

        if len(objects) == 0: objects = self.classification
        objectInfo = []
        if len(classIds) != 0:
            for classId, confidence, box, in zip(classIds.flatten(),confs.flatten(),bbox):
                className = self.classification[classId - 1]
                if className in objects:
                    objectInfo.append([box,className])
                    if (draw):
                        cv.rectangle(img,box,color = (0,255,0), thickness =2)
                        cv.putText(img, self.classification[classId-1].upper(),(box[0],box[1]), cv.FONT_HERSHEY_COMPLEX, 1, (0,255,0),2)
                        cv.putText(img,str(round(confidence*100,2)),(box[1], box[0]), cv.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
        return img, objectInfo
    
    def update_label(self, label):
        self.label = label

    def startCam(self):
        self.cap.set(3,480)
        self.cap.set(4,480)
        while True:
            success, img = self.cap.read()
            result, objectInfo = self.getObject(img,0.70,0.2, objects = ['person'])
            print(object)
            
            # print(objectInfo)
            if objectInfo == []:
                print("I found nothing")
            else:
                print("I found something")
                print(objectInfo[0])
                print(objectInfo[0][1])
                self.label = objectInfo[0][1]

            cv.imshow("ObjectDetection",img)
            cv.waitKey(1)

if __name__ == "__main__":
    camera = Cam()
    camera.startCam()




