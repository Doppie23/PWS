from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()

#hoek is nu wel redelijk (letop min angle mag niet meer dan ong -20)
servo = AngularServo(18, min_angle=-40, max_angle=27, min_pulse_width=0.0010, max_pulse_width=0.0018, pin_factory=factory)


def Stuurhoek(hoek):
    #code voor hoek
    servo.angle = hoek
    print(hoek)
    
#Stuurhoek(-15)