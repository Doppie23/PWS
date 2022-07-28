import cv2
import numpy as np

def hsvkleur(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # cv2.imshow("hsv", hsv)
    return hsv

def paarsalleen(hsvimg):
    lower_blue = np.array([60, 40, 40])
    upper_blue = np.array([150, 255, 255])
    mask = cv2.inRange(hsvimg, lower_blue, upper_blue)
    return mask

def cannyedge(mask):
    edges = cv2.Canny(mask, 200, 400)
    return edges

def cropimg(edges):
    # print(frame.shape)
    crop = edges[240:480, 0:640] #gebruik print hierboven voor getallen
    cropgoed = cv2.copyMakeBorder(crop, top=240, bottom = 0, left = 0, right = 0, borderType=cv2.BORDER_CONSTANT) # om hem op goede plek te zetten, pas de top aan
    return cropgoed

def lijnendetect(canny):
    # getal moeten miss nog aangepast is trial en error
    rho = 1
    angle = np.pi / 180
    min_threshold = 15  # minimum stemmen om te tellen als lijn
    lijnen = cv2.HoughLinesP(canny, rho, angle, min_threshold, np.array([]), 
                                minLineLength=8, maxLineGap=10)
    return lijnen


camera = 1

video = cv2.VideoCapture(camera)
while True:
    _, frame = video.read()
    hsvimg = hsvkleur(frame)
    mask = paarsalleen(hsvimg)
    canny = cannyedge(mask)
    crop = cropimg(canny)
    lijnen = lijnendetect(crop)
    print(lijnen)

    # alle imshow dingen:

    # om lijnen van hough te laten zien
    if lijnen is not None:
        for line in lijnen:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
    cv2.imshow("hough", frame)
    # cv2.imshow("mask", mask)
    cv2.imshow("crop", crop)
    cv2.imshow("canny", canny)



    #esc om te stoppen
    key = cv2.waitKey(1)
    if key == 27:
        break
video.release()
cv2.destroyAllWindows()