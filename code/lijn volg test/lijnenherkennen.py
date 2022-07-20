import cv2
import numpy as np

video = cv2.VideoCapture(0)

while True:
    _, orig_frame = video.read()
    #weet niet wat dit doet maar zal vast geod zijn
    if not _:
        video = cv2.VideoCapture(0)
        continue
    #eerste blurren want keol
    frame = cv2.GaussianBlur(orig_frame, (5, 5), 0)
    #canny edge detect
    edges = cv2.Canny(frame, 75, 150)
    #dan de lijnen tekenen
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, maxLineGap=100) #laatste getal is sensitiviteit
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
    #resultaat laten zien
    cv2.imshow("frame", frame)
    cv2.imshow("edges", edges)

    #escape om af te sluiten
    key = cv2.waitKey(1)
    if key == 27:
        break
video.release()
cv2.destroyAllWindows()