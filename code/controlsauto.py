from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()

#hoek is nu wel redelijk (letop min angle mag niet meer dan ong -20)
servo = AngularServo(17, min_angle=-40, max_angle=27, min_pulse_width=0.0010, max_pulse_width=0.0018, pin_factory=factory)


def Stuurhoek(hoek):
    #code voor hoek
    servo.angle = hoek
    print(hoek)
    
Stuurhoek(-15)
    
#moet eerst wel setup runnen, staat hieronder
def Motor(gas):
    t.ChangeDutyCycle(gas)
    print(throttle)
    
def setup():
    sleep(1)
    IO.setmode(IO.BCM)
    IO.setup(18, IO.OUT)
    t=IO.PWM(18,100)
    throttle = 14
    t.start(throttle)
    input("wacht op geluid en druk dan op enter")
    
def cleanup():
    IO.setmode(IO.BCM)
    IO.setup(18, IO.OUT)
    IO.setup(17, IO.OUT)
    IO.cleanup()