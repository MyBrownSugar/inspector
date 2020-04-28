import cv2 as cv
import time

cap = cv.VideoCapture(0);

i = 0

while (True):
    time.sleep(0.05)
    ret, frame = cap.read()
    if i==0:
        i = 1
        print(ret)
    cv.imshow('frame', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()