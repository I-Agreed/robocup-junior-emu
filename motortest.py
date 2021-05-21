from gpiozero import PWMOutputDevice, DigitalOutputDevice
from time import sleep

enAPin = 12
enBPin = 13
in1Pin = 7
in2Pin = 8
in3Pin = 9
in4Pin = 10

enA = PWMOutputDevice(enAPin)
enB = PWMOutputDevice(enBPin)
in1 = DigitalOutputDevice(in1Pin)
in2 = DigitalOutputDevice(in2Pin)
in3 = DigitalOutputDevice(in3Pin)
in4 = DigitalOutputDevice(in4Pin)

enA.value = 1
enB.value = 1
in1.on()
in2.off()
in3.on()
in4.off()

sleep(5)
