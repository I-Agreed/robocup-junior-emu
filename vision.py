from typing import Tuple
import cv2
import numpy as np
import threading
import math
from config import Config


class Vision:
    def __init__(
        self,
        config: Config,
    ):
        self.cap = cv2.VideoCapture(config.vision.camera.vidSource)
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, 100)
        self.focalLength = config.vision.camera.focalLength
        self.fov = config.vision.camera.fov
        self.camHeight = config.vision.camera.height

        self.ballRange = config.vision.ranges.ball
        self.yellowGoalRange = config.vision.ranges.yellowGoal
        self.blueGoalRange = config.vision.ranges.blueGoal

        self.ballRadius = config.vision.ballRadius
        self.img = self.readCam()
        threading.Thread(target=self.readCamThread)

    def readCam(self):
        return cv2.cvtColor(self.cap.read(), cv2.COLOR_BGR2HSV)

    def readCamThread(self):
        while True:
            self.img = self.readCam()

    def makeBallMask(self, img):
        return cv2.inRange(img, self.ballRange.minVals, self.ballRange.maxVals)

    def makeYellowGoalMask(self, img):
        return cv2.inRange(img, self.yellowGoalRange.minVals, self.yellowGoalRange.maxVals)

    def makeBlueGoalMask(self, img):
        return cv2.inRange(img, self.blueGoalRange.minVals, self.blueGoalRange.maxVals)

    def findRectCoords(self, mask, areaThresh: int):
        contours, hierarchy = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
        )
        for cnt in contours:
            if cv2.contourArea(cnt) > areaThresh:
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                return cv2.boundingRect(approx)
                # Returns x, y, width and height in *pixels*
                # Don't forget that the pixel dimensions are in relation to the panorama image, not the 360 image

    def findDistance(self, coords: Tuple[int]):
        angleOfBall = coords[2] / self.img.shape[0] * self.fov
        return self.ballRadius / math.tan(math.radians(angleOfBall / 2)) / 1000
