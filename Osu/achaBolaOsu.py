import cv2
import sys
import numpy as np
from lib.kukaMov import Kuka
from math import sqrt, pi
import lib.funcKukacador as funcKukacador

# ---------------------------------------------Setup opencv------------------------------------------------------
path = 'C:/Users/gabri/OneDrive/Documents/ProjetoVM/imgs_2'

# Set up the detector with default parameters.
params = cv2.SimpleBlobDetector_Params()
# Set blob color (0=black, 255=white)
params.filterByColor = True
params.blobColor = 255
# Filter by Area
params.filterByArea = True
params.minArea = 550
params.maxArea = 3500
# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.7
params.maxCircularity = 1.2

params.filterByConvexity = False

params.filterByInertia = False

detector = cv2.SimpleBlobDetector_create(params)

kernel = np.ones((11, 11))

# ---------------------------------------trata----------------------------------------
frame_raw = cv2.imread('imgOsu\\osu_10.bmp')
print(frame_raw.shape)
frame = frame_raw.copy()
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# Apply thresholding to remove noise
th = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
# Find contours of objects
contours, hierarchy = cv2.findContours(
    th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# ---------------------------------cria imagem com circulos detectados-------------------------------
area = np.zeros((frame.shape[0], frame.shape[1]), dtype=np.uint8)
img_out = np.zeros((frame.shape[0], frame.shape[1]), dtype=np.uint8)
cv2.drawContours(area, contours, -1, color=(255),
                 thickness=cv2.FILLED)
KP = detector.detect(area)
print(len(KP))
for KPi in KP:
    x, y = KPi.pt[0], KPi.pt[1]
    d = KPi.size
    kpArea = pi*d**2/4
    print(kpArea)
# ---------------------------------------------Mostra imagens-----------------------------------------
img_with_kp = cv2.drawKeypoints(img_out, KP, np.array(
    []), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
# Show keypoints
cv2.imshow("Keypoints", img_with_kp)
# Display the resulting frame
cv2.imshow('frame', frame)
cv2.imshow('detects', area)
# Exit loop if 'q' is pressed
cv2.waitKey(0)
