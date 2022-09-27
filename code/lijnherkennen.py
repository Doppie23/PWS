import cv2
import numpy as np
import math

def hsvkleur(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # cv2.imshow("hsv", hsv)
    return hsv

def paarsalleen(hsvimg):
    # lower_blue = np.array([100, 5, 81]) #hsv codes maar dan gehalveerd
    # upper_blue = np.array([180, 255, 255])
    # mask = cv2.inRange(hsvimg, lower_blue, upper_blue)
    min_blue = 118
    min_green = 14
    min_red = 107
    max_blue = 255
    max_green = 49
    max_red = 177
    
    mask = cv2.inRange(hsvimg, (min_blue, min_green, min_red), (max_blue, max_green, max_red))
    return mask

def cannyedge(mask):
    edges = cv2.Canny(mask, 200, 400)
    return edges

def cropimg(edges, frame):
    height, width, _ = frame.shape
    y = height
    y5 = int(height/2)
    x = width
    crop = edges[y5:y, 0:x] 
    cropgoed = cv2.copyMakeBorder(crop, top=y5, bottom = 0, left = 0, right = 0, borderType=cv2.BORDER_CONSTANT) # om hem op goede plek te zetten
    return cropgoed

def lijnendetect(canny):
    # getal moeten miss nog aangepast is trial en error
    rho = 1
    angle = np.pi / 180
    min_threshold = 20  # minimum stemmen om te tellen als lijn
    lijnen = cv2.HoughLinesP(canny, rho, angle, min_threshold, np.array([]), 
                                minLineLength=60, maxLineGap=60)
    return lijnen

def average(frame, line_segments):
    """
    dit maakt van de meerdere lijnen maar twee lijnen
    als alle hoeken < 0 dan alleen links
    als alle hoeken > 0 dan alleen rechts
    """
    lane_lines = []
    if line_segments is None:
        return lane_lines

    height, width, _ = frame.shape
    left_fit = []
    right_fit = []

    boundary = 1/3
    left_region_boundary = width * (1 - boundary)  # linker lijnen alleen op 2/3 linker helft scherm
    right_region_boundary = width * boundary # zelfde alleen dan voor rechts

    for line_segment in line_segments:
        for x1, y1, x2, y2 in line_segment:
            if x1 == x2:
                continue
            fit = np.polyfit((x1, x2), (y1, y2), 1)
            slope = fit[0]
            intercept = fit[1]
            if slope < 0:
                if x1 < left_region_boundary and x2 < left_region_boundary:
                    left_fit.append((slope, intercept))
            else:
                if x1 > right_region_boundary and x2 > right_region_boundary:
                    right_fit.append((slope, intercept))

    left_fit_average = np.average(left_fit, axis=0)
    if len(left_fit) > 0:
        lane_lines.append(make_points(frame, left_fit_average))

    right_fit_average = np.average(right_fit, axis=0)
    if len(right_fit) > 0:
        lane_lines.append(make_points(frame, right_fit_average))
    return lane_lines

def make_points(frame, line): 
    height, width, _ = frame.shape
    slope, intercept = line
    y1 = height
    y2 = int(y1 * 1 / 2)

    x1 = max(-width, min(2 * width, int((y1 - intercept) / slope)))
    x2 = max(-width, min(2 * width, int((y2 - intercept) / slope)))
    return [[x1, y1, x2, y2]]

def display_lines(frame, lines, line_color=(0, 255, 0), line_width=10):
    line_image = np.zeros_like(frame)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), line_color, line_width)
    line_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    return line_image

def stuurhoek(frame, lane_lines):
    if len(lane_lines) == 0: # geen lijnen
        return 0

    height, width, _ = frame.shape
    if len(lane_lines) == 1: # ziet maar 1 lijn
        x1, _, x2, _ = lane_lines[0][0]
        x_offset = x2 - x1
    else:
        _, _, links_x2, _ = lane_lines[0][0]
        _, _, rechts_x2, _ = lane_lines[1][0]
        mid = int(width / 2) #meot camera wel in het midden zitten
        x_offset = (links_x2 + rechts_x2) / 2 - mid

    y_offset = int(height / 2)

    stuur_hoek_rad = math.atan(x_offset / y_offset)  
    stuur_hoek = int(stuur_hoek_rad * 180.0 / math.pi)
    return stuur_hoek

def stuurhoek_laten_zien(frame, stuurhoek, line_color=(0,0,255), line_width=10):
    richting = np.zeros_like(frame)
    height, width, _ = frame.shape
    stuur_hoek_rad = (stuurhoek+90)/180*math.pi

    x1 = int(width / 2)
    y1 = height
    x2 = int(x1 - height / 2 / math.tan(stuur_hoek_rad))
    y2 = int(height / 2)

    cv2.line(frame, (x1, y1), (x2, y2), line_color, line_width)
    richting = cv2.addWeighted(frame, 0.8, richting, 1, 1)
    return richting

def stabilize_stuurhoek(curr_stuurhoek, new_stuurhoek, num_lijnen, max_hoek_verandering_twee_lijnen=10, max_hoek_verandering_een_lijn=7):
    curr_stuurhoek += 90
    new_stuurhoek += 90
    
    if num_lijnen == 2 :
        max_hoek_verandering = max_hoek_verandering_twee_lijnen
    else :
        max_hoek_verandering = max_hoek_verandering_een_lijn
    
    hoek_verandering = new_stuurhoek - curr_stuurhoek
    if abs(hoek_verandering) > max_hoek_verandering:
        stabilized_stuurhoek = int(curr_stuurhoek
                                        + max_hoek_verandering * hoek_verandering / abs(hoek_verandering))
    else:
        stabilized_stuurhoek = new_stuurhoek

    stabilized_stuurhoek -= 90

    return stabilized_stuurhoek



camera = 0

video = cv2.VideoCapture(camera)

def lijn_volgen():
    _, frame = video.read()
    hsvimg = hsvkleur(frame)
    mask = paarsalleen(hsvimg)
    canny = cannyedge(mask)
    crop = cropimg(canny, frame)
    lijnen = lijnendetect(crop)
    averaged_lines = average(frame, lijnen)
    lane_lines_image = display_lines(frame, averaged_lines)
    hoek = stuurhoek(frame, averaged_lines)
    # print(hoek)
    pijlhoek = stuurhoek_laten_zien(lane_lines_image, hoek)
    

    # alle imshow dingen:

    # om lijnen van hough te laten zien
    if lijnen is not None:
        for line in lijnen:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
    
    # cv2.imshow("hough", frame)
    # cv2.imshow("hsv", hsvimg)
    # cv2.imshow("mask", mask)
    # cv2.imshow("crop", crop)
    # cv2.imshow("canny", canny)
    # cv2.imshow("lane lines", lane_lines_image)
    
    return hoek, averaged_lines, lane_lines_image


    #esc om te stoppen
#     key = cv2.waitKey(1)
#     if key == 27:
#         break
# video.release()
# cv2.destroyAllWindows()

class lijn_volger:
    def __init__(self, beginhoek = 0):
        self.curr_hoek = beginhoek

    def stabhoek(self):
        hoek, averaged_lines, lane_lines_image = lijn_volgen()
        self.curr_hoek = stabilize_stuurhoek(self.curr_hoek, hoek, num_lijnen=averaged_lines)
        # print(self.curr_hoek)
        cv2.imshow("lane lines", lane_lines_image)
        return self.curr_hoek