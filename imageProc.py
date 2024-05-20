import cv2 as cv
import numpy as np

def pega_mascara_vermelha(img_hsv):
    __red_lower = np.array([0, 100, 50], dtype=np.uint8)
    __red_upper = np.array([10, 255, 255], dtype=np.uint8)
    __red_mask1 = cv.inRange(img_hsv, __red_lower, __red_upper)
    __red_lower = np.array([170, 100, 50], dtype=np.uint8)
    __red_upper = np.array([180, 255, 255], dtype=np.uint8)
    __red_mask2 = cv.inRange(img_hsv, __red_lower, __red_upper)
    red_mask = __red_mask1+__red_mask2
    return red_mask

def calibrate(img)->float:
  img_hsv = cv.cvtColor(img,cv.COLOR_BGR2HSV)
  red_mask = pega_mascara_vermelha(img_hsv)

 
