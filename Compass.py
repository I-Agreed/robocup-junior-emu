from typing import Tuple
from i2clibraries import i2c_hmc5883l

class Compass:
    def __init__(self, i2cport: int = 1, declination: Tuple[int] = (12, 40)):
        self.compass = i2c_hmc5883l.i2c_hmc5883l(i2cport)
        self.compass.setContinuousMode()
        self.compass.setDeclination(declination[0], declination[1])
    # TODO: make this
