import cv2
import numpy as np
from collections import deque

def func(a):
    pass

cv2.namedWindow("Editing Tools")
cv2.createTrackbar("Minimum Hue", "Editing Tools", 0, 179, func)
cv2.createTrackbar("Maximum Hue", "Editing Tools", 179, 179, func)
cv2.createTrackbar("Minimum Saturation", "Editing Tools", 130, 255, func)
cv2.createTrackbar("Maximum Saturation", "Editing Tools", 255, 255, func)
cv2.createTrackbar("Minimum Value", "Editing Tools", 55, 255, func)
cv2.createTrackbar("Maximum Value", "Editing Tools", 200, 255, func)
vid=cv2.VideoCapture(0)
kernel=np.ones((3, 3))

b=[deque(maxlen=1024)]
g=[deque(maxlen=1024)]
r=[deque(maxlen=1024)]

b_id=0
g_id=0
r_id=0

colors=[(0, 0, 255), (0, 255, 0), (255, 0, 0)]
color_id=0

paintWindow=np.zeros((480, 640, 3))+255

while True:
    success, frame=vid.read()
    frame=cv2.flip(frame, 1)
    minHue=cv2.getTrackbarPos("Minimum Hue", "Editing Tools")
    maxHue=cv2.getTrackbarPos("Maximum Hue", "Editing Tools")
    minSat=cv2.getTrackbarPos("Minimum Saturation", "Editing Tools")
    maxSat=cv2.getTrackbarPos("Maximum Saturation", "Editing Tools")
    minVal=cv2.getTrackbarPos("Minimum Value", "Editing Tools")
    maxVal=cv2.getTrackbarPos("Maximum Value", "Editing Tools")

    min=np.array([minHue, minSat, minVal])
    max=np.array([maxHue, maxSat, maxVal])

    mask=cv2.inRange(cv2.cvtColor(frame, cv2.COLOR_BGR2HSV), min, max)
    mask=cv2.erode(mask, kernel, iterations=5)
    mask=cv2.dilate(mask, kernel, iterations=10)

    cv2.rectangle(frame, (20, 10), (140, 100), (0, 0, 0), cv2.FILLED)
    cv2.putText(frame, "Clear All", (45, 55), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
    cv2.rectangle(frame, (180, 10), (300, 100), (0, 0, 255), cv2.FILLED)
    cv2.putText(frame, "Red", (225, 55), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
    cv2.rectangle(frame, (340, 10), (460, 100), (0, 255, 0), cv2.FILLED)
    cv2.putText(frame, "Green", (375, 55), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
    cv2.rectangle(frame, (500, 10), (620, 100), (255, 0, 0), cv2.FILLED)
    cv2.putText(frame, "Blue", (540, 55), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

    cv2.rectangle(paintWindow, (20, 10), (140, 100), (0, 0, 0), cv2.FILLED)
    cv2.putText(paintWindow, "Clear All", (45, 55), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
    cv2.rectangle(paintWindow, (180, 10), (300, 100), (0, 0, 255), cv2.FILLED)
    cv2.putText(paintWindow, "Red", (225, 55), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
    cv2.rectangle(paintWindow, (340, 10), (460, 100), (0, 255, 0), cv2.FILLED)
    cv2.putText(paintWindow, "Green", (375, 55), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
    cv2.rectangle(paintWindow, (500, 10), (620, 100), (255, 0, 0), cv2.FILLED)
    cv2.putText(paintWindow, "Blue", (540, 55), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

    cnts,_ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    center = None

    if len(cnts)>0:
        cnt=sorted(cnts, key=cv2.contourArea, reverse=True)[0]
        ((x,y), radius)=cv2.minEnclosingCircle(cnt)
        cv2.circle(frame, (int(x), int(y)), int(radius), (255, 255, 255), thickness=2)

        M = cv2.moments(cnt)
        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

        if center[1] <= 100:
            if 20 <= center[0] <= 140: # Clear Button
                b = [deque(maxlen=512)]
                g = [deque(maxlen=512)]
                r = [deque(maxlen=512)]
    
                b_id = 0
                g_id = 0
                r_id = 0

                paintWindow[:,:,:] = 255
            elif 180 <= center[0] <= 300:
                    color_id = 0 # Red
            elif 340 <= center[0] <= 460:
                    color_id = 1 # Green
            elif 500 <= center[0] <= 620:
                    color_id = 2 # Blue
        else :
            if color_id == 0:
                r[r_id].appendleft(center)
            elif color_id == 1:
                g[g_id].appendleft(center)
            elif color_id == 2:
                b[r_id].appendleft(center)
    else:
        r.append(deque(maxlen=1024))
        r_id += 1
        g.append(deque(maxlen=1024))
        g_id += 1
        b.append(deque(maxlen=1024))
        b_id += 1

    points = [r, g, b]
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k - 1] is None or points[i][j][k] is None:
                    continue
                cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)

    cv2.imshow("Frame", frame)
    cv2.imshow("Paint Window", paintWindow)
    # cv2.imshow("Mask", mask)
    if cv2.waitKey(1):
        continue