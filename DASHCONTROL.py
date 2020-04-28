import cv2
import numpy as np
import time

if __name__ == '__main__':
    def nothing(*arg):
        pass

cv2.namedWindow("resultG")  # создаем главное окно
cv2.namedWindow("resultR")
cv2.namedWindow("resultB")
cv2.namedWindow("camera")
cv2.namedWindow("Result")

cv2.namedWindow("settings for front green")  # создаем окно настроек
cv2.namedWindow("settings for front red")  # создаем окно настроек
cv2.namedWindow("settings for back blue")  # создаем окно настроек

cap = cv2.VideoCapture(1);

# создаем 6 бегунков для настройки начального и конечного цвета фильтра
cv2.createTrackbar('h1', 'settings for front green', 0, 255, nothing)
cv2.createTrackbar('s1', 'settings for front green', 0, 255, nothing)
cv2.createTrackbar('v1', 'settings for front green', 0, 255, nothing)
cv2.createTrackbar('h2', 'settings for front green', 255, 255, nothing)
cv2.createTrackbar('s2', 'settings for front green', 255, 255, nothing)
cv2.createTrackbar('v2', 'settings for front green', 255, 255, nothing)

cv2.createTrackbar('h1', 'settings for front red', 0, 255, nothing)
cv2.createTrackbar('s1', 'settings for front red', 0, 255, nothing)
cv2.createTrackbar('v1', 'settings for front red', 0, 255, nothing)
cv2.createTrackbar('h2', 'settings for front red', 255, 255, nothing)
cv2.createTrackbar('s2', 'settings for front red', 255, 255, nothing)
cv2.createTrackbar('v2', 'settings for front red', 255, 255, nothing)

cv2.createTrackbar('h1', 'settings for back blue', 0, 255, nothing)
cv2.createTrackbar('s1', 'settings for back blue', 0, 255, nothing)
cv2.createTrackbar('v1', 'settings for back blue', 0, 255, nothing)
cv2.createTrackbar('h2', 'settings for back blue', 255, 255, nothing)
cv2.createTrackbar('s2', 'settings for back blue', 255, 255, nothing)
cv2.createTrackbar('v2', 'settings for back blue', 255, 255, nothing)

crange = [0, 0, 0, 0, 0, 0]
switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'settings for front green',0,1,nothing)

while True:
    flag, img = cap.read()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # считываем значения бегунков
   # h1 = cv2.getTrackbarPos('h1', 'settings')
   # s1 = cv2.getTrackbarPos('s1', 'settings')
   # v1 = cv2.getTrackbarPos('v1', 'settings')
   # h2 = cv2.getTrackbarPos('h2', 'settings')
   # s2 = cv2.getTrackbarPos('s2', 'settings')
   # v2 = cv2.getTrackbarPos('v2', 'settings')

    h1G = cv2.getTrackbarPos('h1', 'settings for front green')
    s1G = cv2.getTrackbarPos('s1', 'settings for front green')
    v1G = cv2.getTrackbarPos('v1', 'settings for front green')
    h2G = cv2.getTrackbarPos('h2', 'settings for front green')
    s2G = cv2.getTrackbarPos('s2', 'settings for front green')
    v2G = cv2.getTrackbarPos('v2', 'settings for front green')

    h1R = cv2.getTrackbarPos('h1', 'settings for front red')
    s1R = cv2.getTrackbarPos('s1', 'settings for front red')
    v1R = cv2.getTrackbarPos('v1', 'settings for front red')
    h2R = cv2.getTrackbarPos('h2', 'settings for front red')
    s2R = cv2.getTrackbarPos('s2', 'settings for front red')
    v2R = cv2.getTrackbarPos('v2', 'settings for front red')

    h1B = cv2.getTrackbarPos('h1', 'settings for back blue')
    s1B = cv2.getTrackbarPos('s1', 'settings for back blue')
    v1B = cv2.getTrackbarPos('v1', 'settings for back blue')
    h2B = cv2.getTrackbarPos('h2', 'settings for back blue')
    s2B = cv2.getTrackbarPos('s2', 'settings for back blue')
    v2B = cv2.getTrackbarPos('v2', 'settings for back blue')

    s = cv2.getTrackbarPos(switch, 'image')

    # формируем начальный и конечный цвет фильтра

    h_minG = np.array((h1G, s1G, v1G), np.uint8)
    h_maxG = np.array((h2G, s2G, v2G), np.uint8)

    h_minR = np.array((h1R, s1R, v1R), np.uint8)
    h_maxR = np.array((h2R, s2R, v2R), np.uint8)

    h_minB = np.array((h1B, s1B, v1B), np.uint8)
    h_maxB = np.array((h2B, s2B, v2B), np.uint8)

    #h_min = np.array((h1, s1, v1), np.uint8)
    #h_max = np.array((h2, s2, v2), np.uint8)

    # накладываем фильтр на кадр в модели HSV
    threshG = cv2.inRange(hsv, h_minG, h_maxG)
    threshR = cv2.inRange(hsv, h_minR, h_maxR)
    threshB = cv2.inRange(hsv, h_minB, h_maxB)

    cv2.imshow('resultG', threshG)
    cv2.imshow('resultR', threshR)
    cv2.imshow('resultB', threshB)
    cv2.imshow('camera', img)
    dst = cv2.addWeighted(threshG, 1 , threshR, 1, 0)
    cv2.imshow('Result', dst); #cv2.imshow('Result', threshR); cv2.imshow('Result', threshB);

    ch = cv2.waitKey(5)
    if ch == 27:
        break

cap.release()
cv2.destroyAllWindows()