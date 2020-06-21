import cv2
import numpy as np
import math

def nothing(*arg):
    pass

refPt = []
cropping = False
crop_flag = False

def preview(image, output, gray, gray_blurred):
    result1 = np.hstack([gray_blurred, gray])
    result2 = np.hstack([image, output])
    result1 = cv2.cvtColor(result1, cv2.COLOR_GRAY2BGR)
    result = np.hstack([result1, result2])
    result = cv2.resize(result, (2016, 1008))
    if ((cropping == False) & (crop_flag == True)):
        cv2.rectangle(result, refPt[0], refPt[1], (0, 255, 0), 2)
    cv2.imshow('Output', result)

def get_center(detected):
    center = [0,0]
    for k in range(3):
        center[0] = center[0] + detected[k][0]
        center[1] = center[1] + detected[k][1]
    center[0] = int(center[0] / 3)
    center[1] = int(center[1] / 3)
    return center

def get_angle(center, middle):
    if (middle[0]-center[0]) != 0:
        angle = math.atan((middle[1]-center[1])/(middle[0]-center[0]))*180/math.pi
    else:
        angle = 0
    return angle

def get_length(line):
    length = math.sqrt(line[0]*line[0]+line[1]*line[1])
    return length

def get_polygon(event, x, y, flags, param ):
        global refPt, cropping, crop_flag
        # if the left mouse button was clicked, record the starting
        # (x, y) coordinates and indicate that cropping is being
        # performed
        if event == cv2.EVENT_LBUTTONDOWN:
            refPt = [(x, y)]
            cropping = True
        # check to see if the left mouse button was released
        elif event == cv2.EVENT_LBUTTONUP:
            # record the ending (x, y) coordinates and indicate that
            # the cropping operation is finished
            refPt.append((x, y))
            cropping = False
            crop_flag = True




def get_direction(detected):
    length_list = [0,0,0]
    length_list[0] = get_length([detected[0][0]-detected[1][0],detected[0][1]-detected[1][1]])
    length_list[1] = get_length([detected[1][0] - detected[2][0], detected[1][1] - detected[2][1]])
    length_list[2] = get_length([detected[2][0] - detected[0][0], detected[2][1] - detected[0][1]])
    minIndex = length_list.index(min(length_list))
    if minIndex == 0:
        x_l = (detected[0][0] + detected[1][0]) / 2
        y_l = (detected[0][1] + detected[1][1]) / 2
    if minIndex == 1:
        x_l = (detected[1][0] + detected[2][0]) / 2
        y_l = (detected[1][1] + detected[2][1]) / 2
    if minIndex == 2:
        x_l = (detected[2][0] + detected[0][0]) / 2
        y_l = (detected[2][1] + detected[0][1]) / 2
    middle = [int(x_l), int(y_l)]
    return middle

def flow_filter(x, y, detection):
    pass

def prob_filter(x, y, com):
    pass

cv2.namedWindow('Output')
cv2.setMouseCallback("Output", get_polygon)
cv2.createTrackbar('Ratio of the blur', 'Output', 4, 10, nothing)
cv2.createTrackbar('Ratio of the resolution x10', 'Output', 10, 30, nothing)
cv2.createTrackbar('Param1', 'Output', 73, 100, nothing)
cv2.createTrackbar('Param2', 'Output', 23, 100, nothing)
cv2.createTrackbar('Min distance', 'Output', 4, 30, nothing)
cv2.createTrackbar('Min radius', 'Output', 18, 25, nothing)
cv2.createTrackbar('Max radius', 'Output', 25, 30, nothing)

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

            for k in range(3):
                cv2.circle(image, (detected[k][0],detected[k][1]), 8, (0, 0, 0), 4)

            center = get_center(detected)
            cv2.circle(image, (center[0], center[1]), 4, (0, 255, 255), 3)

            middle = get_direction(detected)
            cv2.line(image, (center[0],center[1]), (middle[0],middle[1]), (0, 255, 0), thickness=2)

            angle = get_angle(center, middle)
            cv2.putText(image, str(angle)[:5], (100, 100), cv2.FONT_ITALIC, 4, 255, 3)

            preview(image, output, gray, gray_blurred)
    else:
        preview(image, output, gray, gray_blurred)

    ch = cv2.waitKey(5)
    if ch == 27:
        print('done')
        break

cv2.destroyAllWindows()
exit()
