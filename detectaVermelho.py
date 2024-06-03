import cv2 as cv
import imageProc
import numpy as np
import sys


cap = cv.VideoCapture(cv.CAP_DSHOW)

_, img = cap.read()
# cortando pra ficar só a tela enquadrada
img_cropped = img.copy()[50:-170, 50:-50]
print(img_cropped.shape)
img_calib_hsv = cv.cvtColor(img_cropped, cv.COLOR_BGR2HSV)

red_mask = imageProc.pega_mascara_vermelha(img_calib_hsv)


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
# params.minCircularity = 0.7
# params.maxCircularity = 1.2
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
kernel = np.ones((11, 11), dtype=np.uint8)
red_mask_dilate = cv.dilate(red_mask, kernel)
KP = detector.detect(red_mask_dilate)
print("Nro de blobs: ", len(KP))

calib_points = []

i = 1
for KPi in KP:
    # print("Blob_", i, ": X= ", KPi.pt[0], " Y= ",
    #       KPi.pt[1], " size=", KPi.size**2, " ang=", KPi.angle)

    calib_points.append((KPi.pt[0], KPi.pt[1]))

    i = i+1

print(calib_points)

cv.imshow('original', img)
cv.imshow('cortada', img_cropped)
cv.imshow('mascara vermelha', red_mask)

cv.waitKey(0)
