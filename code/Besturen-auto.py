from gpiozero import AngularServo
from time import sleep

servo = AngularServo(18)

def Stuurhoek(hoek):
    #code voor hoek
    servo.angle = hoek
    print(hoek)