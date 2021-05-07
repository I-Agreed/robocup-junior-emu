import json
from typing import List
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
class MotorConfig:
    pins: List[int]
    angle: int


@dataclass
class CompassConfig:
    pin: int
    declination: List[int]


@dataclass
class VisionConfig:
    camera: CameraConfig
    ranges: Ranges
    ballRadius: int


class Config:
    def __init__(self, path: str = "./config.json"):
        with open(path, "r") as configFile:
            rawConfig = json.loads(configFile.read())

            self.vision = VisionConfig(
                CameraConfig(
                    rawConfig["vision"]["camera"]["height"],
                    rawConfig["vision"]["camera"]["focalLength"],
                    rawConfig["vision"]["camera"]["fov"],
                    rawConfig["vision"]["camera"]["vidSource"],
                ),
                Ranges(
                    ColorRange(
                        np.array(
                            rawConfig["vision"]["ranges"]["blueGoal"]["minVals"],
                        ),
                        np.array(
                            rawConfig["vision"]["ranges"]["blueGoal"]["maxVals"],
                        ),
                    ),
                    ColorRange(
                        np.array(
                            rawConfig["vision"]["ranges"]["yellowGoal"]["minVals"],
                        ),
                        np.array(
                            rawConfig["vision"]["ranges"]["yellowGoal"]["maxVals"],
                        ),
                    ),
                    ColorRange(
                        np.array(
                            rawConfig["vision"]["ranges"]["ball"]["minVals"],
                        ),
                        np.array(
                            rawConfig["vision"]["ranges"]["ball"]["maxVals"],
                        ),
                    ),
                ),
                rawConfig["vision"]["ballRadius"],
            )

            self.compass = CompassConfig(
                rawConfig["compass"]["pin"], rawConfig["compass"]["declination"]
            )

            self.motors = MotorConfig(
                rawConfig["motors"]["pins"], rawConfig["motors"]["angle"]
            )

    def refresh(self):
        self.__init__()


config = Config()
print(config.vision.camera.focalLength)
