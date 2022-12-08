from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
import RPi.GPIO as IO

factory = PiGPIOFactory()

servo = AngularServo(17, min_angle=-35, max_angle=29, min_pulse_width=0.0012, max_pulse_width=0.0018, pin_factory=factory)

def Stuurhoek(hoek):
    servo.angle = hoek