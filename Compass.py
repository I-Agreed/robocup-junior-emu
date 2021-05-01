from typing import Tuple
from i2clibraries import i2c_hmc5883l
import threading


class Compass:
    def __init__(self, i2cport: int = 1, declination: Tuple[int] = (12, 40)):
        self.compass = i2c_hmc5883l.i2c_hmc5883l(i2cport)
        self.compass.setContinuousMode()
        self.compass.setDeclination(declination[0], declination[1])
        self.calibrateCompass()
        threading.Thread(target=self.getRelativeHeadingThread)

    def calibrateCompass(self):
        self.startHeading = self.compass.getHeading()[0]

    def getRelativeHeading(self):
        # TODO: Check if this actually works
        return self.compass.getHeading()[0] - self.startHeading

    def getRelativeHeadingThread(self):
        while True:
            self.relativeHeading = self.getRelativeHeading()