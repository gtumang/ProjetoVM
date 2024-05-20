import cv2 as cv
import imageProc
import numpy as np
import sys

DIST_X_MM = 880
DIST_Y_MM = 492


cap = cv.VideoCapture(cv.CAP_DSHOW)

_, img_calib = cap.read()
img_calib_cropped = img_calib[40:-170, 70:-100]
img_calib_hsv = cv.cvtColor(img_calib_cropped, cv.COLOR_BGR2HSV)

red_mask = imageProc.pega_mascara_vermelha(img_calib_hsv)

cv.imshow('original', img_calib)
cv.imshow('cortada', img_calib_cropped)
cv.imshow('mascara vermalha', red_mask)

# Set up the detector with default parameters.
params = cv.SimpleBlobDetector_Params()
# Set blob color (0=black, 255=white)
params.filterByColor = True
params.blobColor = 255
# Filter by Area
params.filterByArea = False
# params.minArea = 1000
# params.maxArea = 20000
# Filter by Circularity
params.filterByCircularity = False
# params.minCircularity = 0.8
# #params.maxCircularity = 1.2
# Filter by Convexity
params.filterByConvexity = False
# params.minConvexity = 0.87
# params.maxConvexity = 1
# Filter by Inertia
params.filterByInertia = False
# params.minInertiaRatio = 0.01
# params.maxInertiaRatio = 1
# Set up the detector with default parameters.
detector = cv.SimpleBlobDetector_create(params)

# Detect blobs
KP = detector.detect(red_mask)
print("Nro de blobs: ", len(KP))

if len(KP)<4:
    sys.exit()

calib_points = []

i = 1
for KPi in KP:
    # print("Blob_", i, ": X= ", KPi.pt[0], " Y= ",
    #       KPi.pt[1], " size=", KPi.size**2, " ang=", KPi.angle)

    calib_points.append((KPi.pt[0], KPi.pt[1]))

    i = i+1

min_norm = 100000

min_x = 0
min_y = 0

for point in calib_points:
    norm = (point[0]**2+point[1]**2)**(1/2)
    if norm<min_norm:
        min_x = point[0]
        min_y = point[1]

origin = (min_x,min_y)

# print(origin)

p1 = origin
p2 = 0
p3 = 0
p4 = 0
for p in calib_points:
    if p[0] > 100 and p[1] < 100:
        p2 = (p[0],p[1])
    elif p[0]<100 and p[1]>100:
        p3 = (p[0],p[1])
    elif p[0]>100 and p[1]>100:
        p4 = (p[0],p[1])

print(p1,p2,p3,p4)

dist_x_px = p2[0]-p1[0]
dist_y_px = p3[1]-p1[1]

calib_x = DIST_X_MM/dist_x_px
calib_y = DIST_Y_MM/dist_y_px

cv.waitKey(0)
