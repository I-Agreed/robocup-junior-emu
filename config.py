import json
import numpy as np
from dataclasses import dataclass


@dataclass
class ColorRange:
    minVals: np.ndarray
    maxVals: np.ndarray


@dataclass
class Ranges:
    blueGoal: ColorRange
    yellowGoal: ColorRange
    ball: ColorRange


@dataclass
class CameraConfig:
    height: int
    focalLength: int
    fov: int
    vidSource: int


@dataclass
class Pins:
    compass: int
    motorController1: int
    motorController2: int


class Config:
    def __init__(self, path: str = "./config.json"):
        with open(path, "r") as configFile:
            rawConfig = json.loads(configFile.read())
            self.ranges = Ranges(
                ColorRange(
                    np.array(
                        rawConfig["ranges"]["blueGoal"]["minVals"],
                    ),
                    np.array(
                        rawConfig["ranges"]["blueGoal"]["maxVals"],
                    ),
                ),
                ColorRange(
                    np.array(
                        rawConfig["ranges"]["yellowGoal"]["minVals"],
                    ),
                    np.array(
                        rawConfig["ranges"]["yellowGoal"]["maxVals"],
                    ),
                ),
                ColorRange(
                    np.array(
                        rawConfig["ranges"]["ball"]["minVals"],
                    ),
                    np.array(
                        rawConfig["ranges"]["ball"]["maxVals"],
                    ),
                ),
            )

            self.camera = CameraConfig(
                rawConfig["camera"]["height"],
                rawConfig["camera"]["focalLength"],
                rawConfig["camera"]["fov"],
                rawConfig["camera"]["vidSource"],
            )

            self.pins = Pins(
                rawConfig["pins"]["compass"],
                rawConfig["pins"]["motorController1"],
                rawConfig["pins"]["motorController2"],
            )

    def refresh(self):
        self.__init__()


config = Config()
print(config.camera.focalLength)