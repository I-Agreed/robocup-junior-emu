from typing import Tuple
import cv2
import numpy as np


class Vision:
    def __init__(
        self,
        ballMatchRange: Tuple[np.ndarray] = (np.array([14, 29, 178]),
                                             np.array([43, 169, 255])),
        camHeight: int = 150,
        vidSource: int = 0,
    ):
        self.cap = cv2.VideoCapture(vidSource)
        self.ballMatchRange = ballMatchRange
        self.camHeight = camHeight

    def readCam(self):
        #TODO: Unwrap 360 image into panorama image that actually makes sense
        return cv2.cvtColor(self.cap.read(), cv2.COLOR_BGR2HSV)

    def maskImage(self, img):
        return cv2.inRange(img, self.ballMatchRange[0], self.ballMatchRange[1])

    def findBallRect(self, mask):
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            if cv2.contourArea(cnt) > 500:
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                return cv2.boundingRect(
                    approx)  # Returns x, y, width and height in *pixels*
                #TODO: Do some trig magic and get actual distances... somehow