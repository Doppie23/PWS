import cv2

def doNothing(x):
    pass

cv2.namedWindow('Track Bars', cv2.WINDOW_NORMAL)

cv2.createTrackbar('min_blue', 'Track Bars', 0, 255, doNothing)
cv2.createTrackbar('min_green', 'Track Bars', 0, 255, doNothing)
cv2.createTrackbar('min_red', 'Track Bars', 0, 255, doNothing)

cv2.createTrackbar('max_blue', 'Track Bars', 0, 255, doNothing)
cv2.createTrackbar('max_green', 'Track Bars', 0, 255, doNothing)
cv2.createTrackbar('max_red', 'Track Bars', 0, 255, doNothing)

video = cv2.VideoCapture(0)


while True:
    _, frame = video.read()
    # frame = cv2.GaussianBlur(frame, (5,5),10)
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    min_blue = cv2.getTrackbarPos('min_blue', 'Track Bars')
    min_green = cv2.getTrackbarPos('min_green', 'Track Bars')
    min_red = cv2.getTrackbarPos('min_red', 'Track Bars')
    
    max_blue = cv2.getTrackbarPos('max_blue', 'Track Bars')
    max_green = cv2.getTrackbarPos('max_green', 'Track Bars')
    max_red = cv2.getTrackbarPos('max_red', 'Track Bars')
    
    mask = cv2.inRange(hsv_image, (min_blue, min_green, min_red), (max_blue, max_green, max_red))
    
    #imshow
    cv2.imshow('Mask Image', mask)
    cv2.imshow('Base Image', frame)
    cv2.imshow('HSV Image', hsv_image)
    # q om te stoppen
    key = cv2.waitKey(25)
    if key == ord('q'):
        break

# print zodat gelijk kan copypasten in lijnenherkennen.py
print(f'    min_blue = {min_blue}')
print(f'    min_green = {min_green}')
print(f'    min_red = {min_red}')
print(f'    max_blue = {max_blue}')
print(f'    max_green = {max_green}')
print(f'    max_red = {max_red}')

cv2.destroyAllWindows()