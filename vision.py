from typing import List, Tuple
import cv2
import numpy as np


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

    def readCam(self):
        #TODO: Unwrap 360 image into panorama image that actually makes sense
        return cv2.cvtColor(self.cap.read(), cv2.COLOR_BGR2HSV)

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
                return cv2.boundingRect(
                    approx)  # Returns x, y, width and height in *pixels*
                #TODO: Do some trig magic and get actual distances... somehow