import cv2
import numpy as np


def nothing(*arg):
    pass


def preview(image, output, gray, gray_blurred):
    result1 = np.hstack([gray_blurred, gray])
    result2 = np.hstack([image, output])
    result1 = cv2.cvtColor(result1, cv2.COLOR_GRAY2BGR)
    result = np.hstack([result1, result2])
    result = cv2.resize(result, (2016, 1008))
    cv2.imshow('Output', result)

def flow_filter(x, y, detection):
    pass

def prob_filter(x, y, com):
    pass

cv2.namedWindow('Output')
cv2.createTrackbar('Ratio of the blur', 'Output', 4, 10, nothing)
cv2.createTrackbar('Ratio of the resolution x10', 'Output', 10, 30, nothing)
cv2.createTrackbar('Param1', 'Output', 73, 100, nothing)
cv2.createTrackbar('Param2', 'Output', 23, 100, nothing)
cv2.createTrackbar('Min distance', 'Output', 4, 20, nothing)
cv2.createTrackbar('Min radius', 'Output', 2, 15, nothing)
cv2.createTrackbar('Max radius', 'Output', 15, 30, nothing)

cam = cv2.VideoCapture('http://192.168.0.117:8080/video')
log = cv2.imread('nodata.png')
detected =[ [-1, -1] , [-1, -1], [-1, -1] ]

while True:

    flag, image = cam.read()

    if flag == False:
        cv2.imshow('Output', log)
        ch = cv2.waitKey(5)
        if ch == 27:
            break
        continue

    output = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blur_ratio = cv2.getTrackbarPos('Ratio of the blur', 'Output')
    res_ratio = cv2.getTrackbarPos('Ratio of the resolution x10', 'Output')
    par1 = cv2.getTrackbarPos('Param1', 'Output')
    par2 = cv2.getTrackbarPos('Param2', 'Output')
    min_dist = cv2.getTrackbarPos('Min distance', 'Output')
    min_rad = cv2.getTrackbarPos('Min radius', 'Output')
    max_rad = cv2.getTrackbarPos('Max radius', 'Output')
    res_ratio = res_ratio / 10

    if blur_ratio == 0:
        blur_ratio = 1

    gray_blurred = cv2.blur(gray, (blur_ratio, blur_ratio))
    # detect circles in the image
    circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, res_ratio, min_dist, param1=par1, param2=par2,
                               minRadius=min_rad, maxRadius=max_rad)
    # ensure at least some circles were found

    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
        # loop over the (x, y) coordinates and radius of the circles
        i = 0
        for (x, y, r) in circles:
            if i == 0:
                i = 1
                x1 = x
                y1 = y
                x0 = x1
                y0 = y1
                pass
            else:
                cv2.line(output, (x1, y1), (x, y), (0, 255, 0), thickness=2)
                x1 = x
                y1 = y
            cv2.circle(output, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

            point_flag = True
            for k in range(3):
                if point_flag:
                    for delta in range(7):
                        if ((x == detected[k][0] - 3 + delta) or (y == detected[k][1] - 5 + delta)):
                            point_flag = False
                            break
            if point_flag:
                del detected[0]
                detected.append([x, y])

            for k in range(3):
                cv2.circle(image, (detected[k][0], detected[k][1]), 4, (255, 0, 255), 3)

            preview(image, output, gray, gray_blurred)
    else:
        preview(image, output, gray, gray_blurred)

    ch = cv2.waitKey(5)
    if ch == 27:
        print('done')
        break

cv2.destroyAllWindows()
exit()
