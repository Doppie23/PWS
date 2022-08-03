from lijnherkennenorig import lijn_volger
import cv2


hoek = lijn_volger(0) #is om beginhoek op 0 te zetten moet dus wel eerst nog gedaan worden

gas = 14.9

while True:
    stuurhoek = hoek.stabhoek()

    if stuurhoek < -20:
        stuurhoek = -20
        if gas != 14.7:
            gas = 14.7
    elif stuurhoek > 27:
        stuurhoek = 27
        if gas != 14.7:
            gas = 14.7
    elif gas == 14.7 and stuurhoek < 27 and stuurhoek > -20:    # om gas weer terug te zetten als de hoek weer in servo range zit
        gas = 14.9

    print("hoek:", stuurhoek, "gas:", gas)
    



    key = cv2.waitKey(1)
    if key == 27:
        break
cv2.destroyAllWindows()

