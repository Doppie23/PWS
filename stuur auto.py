from gpiozero import AngularServo
from time import sleep

#min en max pulse width moeten miss nog getuned worden
servo = AngularServo(18, min_pulse_width=0.0008, max_pulse_width=0.0020)

while True:
    #angle is 45 want dat is de angle van de servo
    servo.angle = 45
    sleep(2)
    servo.angle = 0
    sleep(2)
    servo.angle = -45
    sleep(2)
    servo.angle = 0
    sleep(2)
