"""
is om te testen of alle values in lijnherkennen.py goed zijn
"""
from lijnherkennen import lijn_volgen
import cv2

cap = cv2.VideoCapture(2)

while True:
    _, img = cap.read()
    lijn_volgen(img) #alle imshows uncommenten door in deze functie (progamertip selecteer de regels en druk dan ctrl + /)
    key = cv2.waitKey(1)
    if key == 27:
        break
cv2.destroyAllWindows()
