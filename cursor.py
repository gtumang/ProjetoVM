from lib.kukaMov import Kuka
import lib.funcKukacador as funcKukacador
import time
import numpy as np
from math import cos, sin, pi, sqrt
import sys
import cv2

DIST_Y_ROB = 865  # mm

alpha = -pi/2

H_tB = np.array([[1,     0,         0,        -60],
                 [0, cos(alpha), -sin(alpha), DIST_Y_ROB],
                 [0, sin(alpha), cos(alpha),   320],
                 [0,     0,         0,        1]])

rob = Kuka('192.168.50.205', 7000)

if rob.connect():
    print("Robô conectado")
    rob.init()
    rob.setVel(40)
    # time.sleep(1)

    cap = cv2.VideoCapture(cv2.CAP_DSHOW)
    fgbg = cv2.createBackgroundSubtractorMOG2()

    lastImagePoint = (0, 0)

    while True:
        # print('a')
        detects = []
        # Capture frame-by-frame
        ret, frame_raw = cap.read()
        frame = frame_raw.copy()[50:-170, 50:-50]

        # Apply background subtraction
        fgmask = fgbg.apply(frame)

        # Apply thresholding to remove noise
        th = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)[1]

        # Find contours of objects
        contours, hierarchy = cv2.findContours(
            th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Loop through detected objects
        last_dist = 10000
        nearestPoint = None
        for contour in contours:
            # Calculate area of object
            area = cv2.contourArea(contour)
            x, y, w, h = cv2.boundingRect(contour)
            # Filter out small objects
            if (w*h > 650) and (w*h < 1500):
                dist = sqrt((lastImagePoint[0]-x)**2+(lastImagePoint[1]-y)**2)
                if dist < last_dist:
                    nearestPoint = (x, y)
                    last_dist = dist

        if nearestPoint is not None:
            imgPoint = nearestPoint
            PosRob = funcKukacador.image2kuka(imgPoint, H_tB)

            if PosRob[0] < rob.x_robo_max and PosRob[0] > rob.x_robo_min and PosRob[2] < rob.z_robo_max and PosRob[2] > rob.z_robo_min:
                rob.setPos(PosRob)

            lastImagePoint = imgPoint

        # Exit loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            rob.close()
            break
