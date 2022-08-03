from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
import RPi.GPIO as IO
import cv2

factory = PiGPIOFactory()

#hoek is nu wel redelijk (letop min angle mag niet meer dan ong -20)
servo = AngularServo(17, min_angle=-40, max_angle=27, min_pulse_width=0.0010, max_pulse_width=0.0018, pin_factory=factory)

def Stuurhoek(hoek):
    #code voor hoek
    servo.angle = hoek

#Stuurhoek(0)

def cleanup():
    IO.setmode(IO.BCM)
    IO.setup(18, IO.OUT)
    IO.setup(17, IO.OUT)
    IO.cleanup()
    cv2.destroyAllWindows()
