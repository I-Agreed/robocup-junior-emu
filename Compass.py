from i2clibraries import i2c_hmc5883l
import threading
from config import Config


class Compass:
    def __init__(self, config: Config):
        self.compass = i2c_hmc5883l.i2c_hmc5883l(config.compass.pin)
        self.compass.setContinuousMode()
        self.compass.setDeclination(*config.compass.declination)
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
