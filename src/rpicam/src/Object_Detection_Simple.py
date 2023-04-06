import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox

vid = cv2.VideoCapture(0)

while True:
    ret,frame = vid.read()
    bbox, label, conf = cv.detect_common_objects(frame)
    out_img = draw_bbox(frame, bbox, label, conf)
    cv2.imshow("Object_Detection", out_img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break



