import cv2
import os
import numpy as np

path = 'C:/Users/gabri/OneDrive/Documents/ProjetoVM/imgs_2'

# Initialize video capture
cap = cv2.VideoCapture(cv2.CAP_DSHOW)

_, img_calib = cap.read()


# Initialize background subtractor
fgbg = cv2.createBackgroundSubtractorMOG2()
detects = []
# Loop through frames

kernel = np.array((7, 7))

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = frame[
        50:-170, 50:-50]

    # Apply background subtraction
    fgmask = fgbg.apply(frame)

    # Apply thresholding to remove noise
    th = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)[1]

    th_open = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel=kernel, iterations=2)
    th_close = cv2.morphologyEx(
        th_open, cv2.MORPH_CLOSE, kernel=kernel, iterations=2)

    # Find contours of objects
    contours, hierarchy = cv2.findContours(
        th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Loop through detected objects
    for contour in contours:
        # Calculate area of object
        area = cv2.contourArea(contour)
        x, y, w, h = cv2.boundingRect(contour)
        # Filter out small objects

    # Display the resulting frame
    cv2.imshow('frame', frame)
    cv2.imshow('detects', th)
    cv2.imshow('detects dilate', th_close)

    # Exit loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and destroy windows
i = 0
# for img in detects:
#     cv2.imwrite(os.path.join(path, f'detect_{i}.png'), img)
#     i += 1

print(len(detects))

cap.release()
cv2.destroyAllWindows()
