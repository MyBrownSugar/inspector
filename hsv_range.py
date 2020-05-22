import cv2
import numpy as np
import time


def nothing(*arg):
    pass


def screenshot(*arg):
    flag, img = cam.read()
    timestr = time.strftime("%d.%m.%Y %H{0}%M{1}%S".format('-', '-'))
    ext = '.png'
    filename = timestr + ext
    cv2.imwrite(filename, img)
    pass


cv2.namedWindow("HSV range")

# cam = cv2.VideoCapture(0);
cam = cv2.VideoCapture('http://192.168.0.117:8080/video')

cv2.createTrackbar('h min', 'HSV range', 0, 255, nothing)
cv2.createTrackbar('h max', 'HSV range', 255, 255, nothing)
cv2.createTrackbar('s min', 'HSV range', 0, 255, nothing)
cv2.createTrackbar('s max', 'HSV range', 255, 255, nothing)
cv2.createTrackbar('v min', 'HSV range', 0, 255, nothing)
cv2.createTrackbar('v max', 'HSV range', 255, 255, nothing)
cv2.createTrackbar('switch', 'HSV range', 0, 1, nothing)
cv2.createTrackbar('screenshot', 'HSV range', 0, 1, screenshot)

log = cv2.imread('nodata.png')

while True:

    flag, img = cam.read()

    if flag == False:
        cv2.imshow('Output', log)
        ch = cv2.waitKey(5)
        if ch == 27:
            break
        continue

    img = cv2.medianBlur(img, 5)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    h1 = cv2.getTrackbarPos('h min', 'HSV range')
    h2 = cv2.getTrackbarPos('h max', 'HSV range')

    s1 = cv2.getTrackbarPos('s min', 'HSV range')
    s2 = cv2.getTrackbarPos('s max', 'HSV range')

    v1 = cv2.getTrackbarPos('v min', 'HSV range')
    v2 = cv2.getTrackbarPos('v max', 'HSV range')

    h_min = np.array((h1, s1, v1), np.uint8)
    h_max = np.array((h2, s2, v2), np.uint8)

    filter = cv2.inRange(hsv, h_min, h_max)

    switch = cv2.getTrackbarPos('switch', 'HSV range')
    if switch == 0:
        filter = cv2.medianBlur(filter, 5)
        filter = cv2.resize(filter, (450, 800))
        cv2.imshow('HSV range', filter)
    else:
        img = cv2.resize(img, (450, 800))
        cv2.imshow('HSV range', img)

    ch = cv2.waitKey(5)
    if ch == 27:
        break

cam.release()
cv2.destroyAllWindows()
exit()
