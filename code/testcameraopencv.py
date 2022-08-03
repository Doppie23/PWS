"""
is om te testen of alle values in lijnherkennen.py goed zijn
"""
from lijnherkennen import lijn_volgen
import cv2

while True:
    lijn_volgen() #alle imshows uncommenten door in deze functie (progamertip selecteer de regels en druk dan ctrl + /)
    key = cv2.waitKey(1)
    if key == 27:
        break
cv2.destroyAllWindows()
