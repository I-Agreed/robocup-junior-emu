from typing import List, Tuple
import cv2
import numpy as np
import threading


class Vision:
    def __init__(
        self,
        yellowGoalRange: Tuple[List[int]],
        blueGoalRange: Tuple[List[int]],
        #TODO: ^- Add default values for these
        ballRange: Tuple[List[int]] = ([14, 29, 178], [43, 169, 255]),
        #TODO: ^- Change these to actual color of competition ball, not a tennis ball
        camHeight: int = 150,
        vidSource: int = 0,
    ):
        self.cap = cv2.VideoCapture(vidSource)
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, 100)
        self.ballRange = (np.array(ballRange[0]), np.array(ballRange[1]))
        self.yellowGoalRange = (np.array(yellowGoalRange[0]),
                                np.array(yellowGoalRange[1]))
        self.blueGoalRange = (np.array(blueGoalRange[0]),
                              np.array(blueGoalRange[1]))
        self.camHeight = camHeight
        self.img = self.readCam()
        threading.Thread(target=self.readCamThread)

    def readCam(self):
        return cv2.cvtColor(self.cap.read(), cv2.COLOR_BGR2HSV)

    def readCamThread(self):
        while True:
            self.img = self.readCam()

    def makeBallMask(self, img):
        return cv2.inRange(img, self.ballMatchRange[0], self.ballMatchRange[1])

    def makeYellowGoalMask(self, img):
        return cv2.inRange(img, self.yellowGoalRange[0],
                           self.yellowGoalRange[1])

    def makeBlueGoalMask(self, img):
        return cv2.inRange(img, self.blueGoalRange[0], self.blueGoalRange[1])

    def findRect(self, mask, areaThresh: int):
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            if cv2.contourArea(cnt) > areaThresh:
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                return cv2.boundingRect(approx)
                # Returns x, y, width and height in *pixels*
                # Don't forget that the pixel dimensions are in relation to the panorama image, not the 360 image
                #TODO: Do some trig magic and get actual distances... somehow