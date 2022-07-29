import cv2
import numpy as np

def hsvkleur(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # cv2.imshow("hsv", hsv)
    return hsv

def paarsalleen(hsvimg):
    lower_blue = np.array([100, 5, 81])
    upper_blue = np.array([180, 255, 255])
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
    min_threshold = 20  # minimum stemmen om te tellen als lijn
    lijnen = cv2.HoughLinesP(canny, rho, angle, min_threshold, np.array([]), 
                                minLineLength=60, maxLineGap=60)
    return lijnen

def average(image, lines):
    left = []
    right = []
    for line in lines:
        print(line)
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        y_int = parameters[1]
        if slope < 0:
            left.append((slope, y_int))
        else:
            right.append((slope, y_int))
    right_avg = np.average(right, axis=0)
    left_avg = np.average(left, axis=0)
    left_line = make_points(image, left_avg)
    right_line = make_points(image, right_avg)
    return np.array([left_line, right_line])

def make_points(frame, line): 
    height, width, _ = frame.shape
    slope, intercept = line
    y1 = height  # bottom of the frame
    y2 = int(y1 * 1 / 2)  # make points from middle of the frame down

    # bound the coordinates within the frame
    x1 = max(-width, min(2 * width, int((y1 - intercept) / slope)))
    x2 = max(-width, min(2 * width, int((y2 - intercept) / slope)))
    return [[x1, y1, x2, y2]]

def display_lines(frame, lines, line_color=(0, 255, 0), line_width=2):
    line_image = np.zeros_like(frame)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), line_color, line_width)
    line_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    return line_image


camera = 1

video = cv2.VideoCapture(camera)
while True:
    _, frame = video.read()
    hsvimg = hsvkleur(frame)
    mask = paarsalleen(hsvimg)
    canny = cannyedge(mask)
    crop = cropimg(canny)
    lijnen = lijnendetect(crop)
    averaged_lines = average(frame, lijnen)
    lane_lines_image = display_lines(frame, averaged_lines)
    

    # alle imshow dingen:

    # om lijnen van hough te laten zien
    if lijnen is not None:
        for line in lijnen:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
    cv2.imshow("hsv", hsvimg)
    cv2.imshow("hough", frame)
    cv2.imshow("mask", mask)
    cv2.imshow("crop", crop)
    cv2.imshow("canny", canny)
    cv2.imshow("lane lines", lane_lines_image)



    #esc om te stoppen
    key = cv2.waitKey(1)
    if key == 27:
        break
video.release()
cv2.destroyAllWindows()