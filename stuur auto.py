from gpiozero import AngularServo
from time import sleep

servo = AngularServo(18, min_pulse_width=0.0008, max_pulse_width=0.0020)

while True:
    #angle is 45 om  de servo heel te houden... kreeg het anders niet goed werkend
    servo.angle = 45
    sleep(2)
    servo.angle = 0
    sleep(2)
    servo.angle = -45
    sleep(2)
    servo.angle = 0
    sleep(2)