import controlsauto as ca
from time import sleep
import RPi.GPIO as IO

#setup
sleep(1)
IO.setmode(IO.BCM)
IO.setup(18, IO.OUT)
t=IO.PWM(18,100)
throttle = 14
t.start(throttle)
input("wacht op geluid en druk dan op enter")

#wielen in het midden
ca.Stuurhoek(0)

#nu vooruit met min snelheid
gas=14.9
t.ChangeDutyCycle(gas)
print(gas)

input("enter voor eindigen")
ca.cleanup()