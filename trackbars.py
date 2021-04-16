import cv2 as cv
from cv2.cv2 import VideoCapture
import numpy as np
from sys import argv

def empty(img):
    pass

def analyse(img):
    imgHsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    hueMin = cv.getTrackbarPos("Hue Min", "TrackBars")
    hueMax = cv.getTrackbarPos("Hue Max", "TrackBars")
    satMin = cv.getTrackbarPos("Sat Min", "TrackBars")
    satMax = cv.getTrackbarPos("Sat Max", "TrackBars")
    valMin = cv.getTrackbarPos("Val Min", "TrackBars")
    valMax = cv.getTrackbarPos("Val Max", "TrackBars")

    minVals = np.array([hueMin, satMin, valMin])
    maxVals = np.array([hueMax, satMax, valMax])
    mask = cv.inRange(imgHsv, minVals, maxVals)
    maskColor = cv.bitwise_and(img, img, mask=mask)

    cv.imshow("Original Image", img)
    cv.imshow("HSV Image", imgHsv)
    cv.imshow("Masked Image", mask)
    cv.imshow("Masked Image with Color", maskColor)
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        cv.destroyAllWindows()
        print("")
        print(f"Minimum Hue: {hueMin}")
        print(f"Maximum Hue: {hueMax}")
        print(f"Minimum Saturation: {satMin}")
        print(f"Maximum Saturation: {satMax}")
        print(f"Minimum Value: {valMin}")
        print(f"Maximum Value: {valMax}")
        exit()

cv.namedWindow("TrackBars")
cv.resizeWindow("TrackBars", 640, 240)
cv.createTrackbar("Hue Min", "TrackBars", 0, 179, empty)
cv.createTrackbar("Hue Max", "TrackBars", 170, 179, empty)
cv.createTrackbar("Sat Min", "TrackBars", 0, 255, empty)
cv.createTrackbar("Sat Max", "TrackBars", 255, 255, empty)
cv.createTrackbar("Val Min", "TrackBars", 0, 255, empty)
cv.createTrackbar("Val Max", "TrackBars", 255, 255, empty)

print("Hit 'q' to quit!")
if not len(argv) >= 2:
    cap = VideoCapture(0)
    cap.set(10, 100)
    while True:
        success, img = cap.read()
        analyse(img)
else:
    while True:
        img = cv.imread(argv[1])
        analyse(img)
