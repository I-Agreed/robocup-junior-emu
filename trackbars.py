import cv2 as cv2
from cv2.cv2 import VideoCapture
import numpy as np
from sys import argv


def empty(img):
    pass


def analyse(img):
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    hueMin = cv2.getTrackbarPos("Hue Min", "TrackBars")
    hueMax = cv2.getTrackbarPos("Hue Max", "TrackBars")
    satMin = cv2.getTrackbarPos("Sat Min", "TrackBars")
    satMax = cv2.getTrackbarPos("Sat Max", "TrackBars")
    valMin = cv2.getTrackbarPos("Val Min", "TrackBars")
    valMax = cv2.getTrackbarPos("Val Max", "TrackBars")

    minVals = np.array([hueMin, satMin, valMin])
    maxVals = np.array([hueMax, satMax, valMax])
    mask = cv2.inRange(imgHsv, minVals, maxVals)
    maskColor = cv2.bitwise_and(img, img, mask=mask)

    cv2.imshow("Original Image", img)
    cv2.imshow("HSV Image", imgHsv)
    cv2.imshow("Masked Image", mask)
    cv2.imshow("Masked Image with Color", maskColor)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        print("")
        print("--- RAW VALUES ---")
        print(f"Minimum Hue: {hueMin}")
        print(f"Minimum Saturation: {satMin}")
        print(f"Minimum Value: {valMin}")
        print(f"Maximum Hue: {hueMax}")
        print(f"Maximum Saturation: {satMax}")
        print(f"Maximum Value: {valMax}")
        print("")
        print("--- PYTHON CODE ---")
        print(f"minVals = np.array([{hueMin}, {satMin}, {valMin}])")
        print(f"maxVals = np.array([{hueMax}, {satMax}, {valMax}])")
        print(f"mask = cv2.inrange(img, minVals, maxVals)")
        exit()


cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", 640, 240)
cv2.createTrackbar("Hue Min", "TrackBars", 0, 179, empty)
cv2.createTrackbar("Hue Max", "TrackBars", 170, 179, empty)
cv2.createTrackbar("Sat Min", "TrackBars", 0, 255, empty)
cv2.createTrackbar("Sat Max", "TrackBars", 255, 255, empty)
cv2.createTrackbar("Val Min", "TrackBars", 0, 255, empty)
cv2.createTrackbar("Val Max", "TrackBars", 255, 255, empty)

print("Hit 'q' to quit!")
if not len(argv) >= 2:
    cap = VideoCapture(0)
    cap.set(cv2.CAP_PROP_BRIGHTNESS, 100)
    while True:
        success, img = cap.read()
        analyse(img)
else:
    while True:
        img = cv2.imread(argv[1])
        analyse(img)
