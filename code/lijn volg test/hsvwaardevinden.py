# https://medium.com/globant/maneuvering-color-mask-into-object-detection-fce61bf891d1


import cv2
#empty function
def doNothing(x):
    pass

#creating a resizable window named Track Bars
cv2.namedWindow('Track Bars', cv2.WINDOW_NORMAL)

#creating track bars for gathering threshold values of red green and blue
cv2.createTrackbar('min_blue', 'Track Bars', 0, 255, doNothing)
cv2.createTrackbar('min_green', 'Track Bars', 0, 255, doNothing)
cv2.createTrackbar('min_red', 'Track Bars', 0, 255, doNothing)

cv2.createTrackbar('max_blue', 'Track Bars', 0, 255, doNothing)
cv2.createTrackbar('max_green', 'Track Bars', 0, 255, doNothing)
cv2.createTrackbar('max_red', 'Track Bars', 0, 255, doNothing)

video = cv2.VideoCapture(2)

#creating a loop to get the feedback of the changes in trackbars
while True:
    #reading the trackbar values for thresholds
    _, frame = video.read()
    frame = cv2.GaussianBlur(frame, (5,5),10)
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    min_blue = cv2.getTrackbarPos('min_blue', 'Track Bars')
    min_green = cv2.getTrackbarPos('min_green', 'Track Bars')
    min_red = cv2.getTrackbarPos('min_red', 'Track Bars')
    
    max_blue = cv2.getTrackbarPos('max_blue', 'Track Bars')
    max_green = cv2.getTrackbarPos('max_green', 'Track Bars')
    max_red = cv2.getTrackbarPos('max_red', 'Track Bars')
    
    #using inrange function to turn on the image pixels where object threshold is matched
    mask = cv2.inRange(hsv_image, (min_blue, min_green, min_red), (max_blue, max_green, max_red))
    #showing the mask image
    cv2.imshow('Mask Image', mask)
    cv2.imshow('Base Image', frame)
    cv2.imshow('HSV Image', hsv_image)
    # checking if q key is pressed to break out of loop
    key = cv2.waitKey(25)
    if key == ord('q'):
        break
#printing the threshold values for usage in detection application
print(f'min_blue {min_blue}  min_green {min_green} min_red {min_red}')
print(f'max_blue {max_blue}  max_green {max_green} max_red {max_red}')
#destroying all windows
cv2.destroyAllWindows()

#trust cam
# min_blue 75  min_green 16 min_red 196
# max_blue 255  max_green 255 max_red 255