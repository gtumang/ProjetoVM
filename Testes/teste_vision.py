import numpy as np
import cv2 as cv
cap = cv.VideoCapture(cv.CAP_DSHOW)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

_, img_zero_raw = cap.read()
img_zero = img_zero_raw[60:-200, 80:-100]
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    img_cropped = frame[60:-200, 80:-100]
    img_sub = cv.subtract(img_cropped, img_zero)
    img_gray = cv.cvtColor(img_sub, cv.COLOR_BGR2GRAY)
    img_gray = cv.equalizeHist(img_gray)
    _, img_thresh = cv.threshold(img_gray, 10, 255, cv.THRESH_BINARY)
    # Display the resulting frame
    cv.imshow('frame', img_thresh)
    if cv.waitKey(1) == ord('q'):
        break
    # When everything done, release the capture
cap.release()
cv.destroyAllWindows()
