import cv2
import sys
import numpy as np
from lib.kukaMov import Kuka
from math import sqrt
import lib.funcKukacador as funcKukacador

#------------------------------------------------Setup robo-------------------------------------------------
rob = Kuka('192.168.50.205',7000)
if not rob.connect():
    print("Nao foi possivel conectar ao Kuka")
    sys.exit()

rob.init()
rob.setVel(75)

#---------------------------------------------Setup opencv------------------------------------------------------
path = 'C:/Users/gabri/OneDrive/Documents/ProjetoVM/imgs_2'

# Initialize video capture
cap = cv2.VideoCapture(cv2.CAP_DSHOW)

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

#---------------------------------------------Variaveis de auxilio------------------------------------------
lastImagePoint = (0, 0)
#--------------------------------------------------Main loop-------------------------------------------------
while True:
    #---------------------------------------Captura frame e trata----------------------------------------
    ret, frame_raw = cap.read()
    # print(frame_raw.shape)
    frame = frame_raw.copy()[50:-170, 50:-50]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Apply thresholding to remove noise
    th = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
    # Find contours of objects
    contours, hierarchy = cv2.findContours(
        th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # ---------------------------------cria imagem com circulos detectados-------------------------------
    area = np.zeros((frame.shape[0], frame.shape[1]), dtype=np.uint8)
    img_out = np.zeros((frame.shape[0], frame.shape[1]), dtype=np.uint8)
    nearestPoint = None
    last_dist = 10000
    cv2.drawContours(area, contours, -1, color=(255),
                     thickness=cv2.FILLED)

    #-----------------------------------------loopa pelos KPis-----------------------------------
    KP = detector.detect(area)
    for KPi in KP:
      x,y = KPi.pt[0],KPi.pt[1]
      dist = sqrt((lastImagePoint[0]-x)**2+(lastImagePoint[1]-y)**2)
      if dist < last_dist:
        nearestPoint = (x, y)
        last_dist = dist

    if nearestPoint is not None:
        imgPoint = nearestPoint
        PosRob = funcKukacador.image2kuka(imgPoint)
        rob.setPos(PosRob)
        lastImagePoint = imgPoint

    #---------------------------------------------Mostra imagens-----------------------------------------
    im_with_keypoints = cv2.drawKeypoints(img_out, KP, np.array(
        []), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    # Show keypoints
    cv2.imshow("Keypoints", im_with_keypoints)
    # Display the resulting frame
    cv2.imshow('frame', frame)
    cv2.imshow('detects', area)
    # Exit loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        rob.close()
        break

cap.release()
cv2.destroyAllWindows()
