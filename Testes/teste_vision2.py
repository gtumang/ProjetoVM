import numpy as np
import cv2 as cv
cap = cv.VideoCapture(cv.CAP_DSHOW)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

_, img = cap.read()
print(img.shape)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    img_cropped = frame[:200, :240]
    # Display the resulting frame
    cv.imshow('frame_cropped', img_cropped)
    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break
    # When everything done, release the capture
cap.release()
cv.destroyAllWindows()
