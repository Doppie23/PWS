from gpiozero import AngularServo
from time import sleep

#max en min pulse width zijn gegokt door te testen
servo = AngularServo(18, min_pulse_width=0.0004, max_pulse_width=0.0023)

while True:
    #angle is 30 want dat is vgm de max angle
    servo.angle = 30
    print("rechts")
    sleep(2)
    servo.angle = 0
    print("mid")
    sleep(2)
    servo.angle = -30
    print("links")
    sleep(2)
    servo.angle = 0
    print("mid")
    sleep(2)
