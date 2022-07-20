from tkinter import Frame
import cv2 as cv
import numpy as np

camera = cv.VideoCapture(0)

while True:
    _, frame = camera.read()

    cv.imshow('Camera', frame)

    edges = cv.Canny(frame, 140, 140)
    cv.imshow('Canny', edges)


    if cv.waitKey(5) == ord('x'):
        break

camera.release()
cv.destroyAllwindows()