from lijnherkennen import lijn_volgen
import cv2

while True:
    lijn_volgen()
    
    key = cv2.waitKey(1)
    if key == 27:
        break
cv2.destroyAllWindows()

