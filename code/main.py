from lijnherkennen import lijn_volger
import cv2
import controlsauto as ca
from time import sleep
import RPi.GPIO as IO

# initialiseren van auto
print("auto aan het initialiseren")
sleep(1)
IO.setmode(IO.BCM)
IO.setup(18, IO.OUT)
t=IO.PWM(18,100)
throttle = 14
t.start(throttle)
input("wacht op geluid van esc druk dan op enter")

ca.Stuurhoek(0)
hoek = lijn_volger(0) #0 is de begin hoek van de servo
input("klaar om te gaan druk op enter")
gas = 14.9
t.ChangeDutyCycle(gas)

while True:
    """
    hoek sturen met opencv
    """
    stuurhoek = hoek.stabhoek()
    
    #zodat de servo niet te ver gaat en als de hoek wel zo groot is gaat de motor langzamer
    if stuurhoek < -20:
        stuurhoek = -20
        gas = 14.7
        t.ChangeDutyCycle(gas)
    elif stuurhoek > 27:
        stuurhoek = 27
        gas = 14.7
        t.ChangeDutyCycle(gas)
    elif gas == 14.7 and stuurhoek < 27 and stuurhoek > -20:    # om gas weer terug te zetten als de hoek weer in servo range zit
        gas = 14.9
        t.ChangeDutyCycle(gas)
    
    ca.Stuurhoek(stuurhoek)
    print("hoek:", stuurhoek, "gas:", gas)

    """
    cleanup (esc om te stoppen)
    """
    key = cv2.waitKey(1)
    if key == 27:
        break
ca.cleanup()