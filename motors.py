from gpiozero import Motor
import math


class Omniwheel:
    def __init__(self, pins, angle, modifier):
        self.pins = pins
        self.motor = Motor(*pins)
        self.angle = angle
        self.tanAngle = (angle + 90) % 360
        self.modifier = modifier

    def set_speed(self, speed):
        if speed > 0:
            self.motor.forward(speed * self.modifier)
        else:
            self.motor.backward(-speed * self.modifier)

    def set(self, speed, angle, turning):
        m = speed * math.cos(math.radians(self.angle - angle)) + turning


class Movement:
    def __init__(self, *pins):  # pins = (pin1, pin2, angle, speedMultiplier)
        self.motors = [Omniwheel(pin[:2], pin[2], pin[3]) for pin in pins]

    def set(self, speed, angle, turning):
        for i in self.motors:
            i.set(speed, angle, turning)


if __name__ == "__main__":
    m = Movement((0, 1, 45, 1), (0, 1, 135, 1), (0, 1, 215, 1), (0, 305, 0, 1))
