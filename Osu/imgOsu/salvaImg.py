import cv2 as cv
import time

cap = cv.VideoCapture(cv.CAP_DSHOW)
cap.set(cv.CAP_PROP_AUTOFOCUS, 0)  # turn the autofocus off

i=0
while i<20:
  _, img_raw = cap.read()
  img = img_raw.copy()[50:-170, 50:-50]
  cv.imwrite(f"imgOsu\\osu_{i}.bmp",img)
  i+=1
  time.sleep(1)