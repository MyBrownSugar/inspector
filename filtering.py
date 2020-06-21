import cv2
import numpy as np
import math

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
flag3 = 1
direction1 = 0
rd = 0
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

            center_x = 0
            center_y = 0
            sm = [0, 0, 0]
            for k in range(3):
                sm[k] = detected[k][0]+detected[k][1]
                cv2.circle(image, (detected[k][0], detected[k][1]), 4, (64, 128, 255), 3)
                center_x=center_x + detected[k][0]
                center_y=center_y + detected[k][1]
            center_x=center_x/3
            center_y=center_y/3
            cv2.circle(image, (int(center_x), int(center_y)), 4, (0, 255, 255), 3)

            ch = [abs(sm[0]-sm[1]),abs(sm[1]-sm[2]),abs(sm[2]-sm[0])]
            minIndex = ch.index(min(ch))
            center_y = int(center_y)
            center_x = int(center_x)
            if minIndex == 0:
                x_l = (detected[0][0]+detected[1][0])/2
                y_l = (detected[0][1]+detected[1][1])/2
                cv2.line(image, (center_x, center_y), (int(x_l), int(y_l)), (0, 255, 0), thickness=2)
            if minIndex == 1:
                x_l = (detected[1][0]+detected[2][0])/2
                y_l = (detected[1][1]+detected[2][1])/2
                cv2.line(image, (center_x, center_y), (int(x_l), int(y_l)), (0, 255, 0), thickness=2)
            if minIndex == 2:
                x_l = (detected[2][0]+detected[0][0])/2
                y_l = (detected[2][1]+detected[0][1])/2
                cv2.line(image, (center_x, center_y), (int(x_l), int(y_l)), (0, 255, 0), thickness=2)
            cv2.line(image, (int(x_l), center_y), (center_x, center_y), (40, 10, 255), thickness=2)
            line1 = [center_x-x_l, center_y-y]
            line2 = [x_l - center_x, 0]
            dist1 = math.sqrt(line1[0]*line1[0]+line1[1]*line1[1])
            dist2 = math.sqrt(line2[0] * line2[0] + line2[1] * line2[1])
            if flag3 < 10:
                flag3=flag3 + 1
                direction1 = direction1 + np.arcsin(dist2/dist1)
            else:
                flag3 = 1
                r_direction = direction1 / 10
                direction1 = 0
                rd = r_direction*180/math.pi
                rd = math.atan((y_l - center_y) / (x_l - center_x))*180/math.pi
            cv2.putText(image, str(rd)[:5], (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 4, 255, 3)



            preview(image, output, gray, gray_blurred)
    else:
        preview(image, output, gray, gray_blurred)

    ch = cv2.waitKey(5)
    if ch == 27:
        print('done')
        break

cv2.destroyAllWindows()
exit()
