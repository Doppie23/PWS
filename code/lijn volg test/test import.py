from lijnherkennen import lijn_volger
import cv2


hoek = lijn_volger(0) #is om beginhoek op 0 te zetten moet dus wel eerst nog gedaan worden


while True:
    hoek.stabhoek()

    key = cv2.waitKey(1)
    if key == 27:
        break
cv2.destroyAllWindows()

