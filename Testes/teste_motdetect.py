import cv2
import os
path = 'C:/Users/gabri/OneDrive/Documents/ProjetoVM/imgs_2'

# Initialize video capture
cap = cv2.VideoCapture(cv2.CAP_DSHOW)

_,img_calib = cap.read()



# Initialize background subtractor
fgbg = cv2.createBackgroundSubtractorMOG2()
detects = []
# Loop through frames
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = frame[40:-170, 70:-100]

    # Apply background subtraction
    fgmask = fgbg.apply(frame)

    # Apply thresholding to remove noise
    th = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)[1]

    # Find contours of objects
    contours, hierarchy = cv2.findContours(
        th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Loop through detected objects
    for contour in contours:
        # Calculate area of object
        area = cv2.contourArea(contour)
        x, y, w, h = cv2.boundingRect(contour)
        # Filter out small objects
        if (w*h > 650) and (w*h < 900):
            cv2.imshow('detect', frame[y:y+h, x:x+w])
            detects.append(frame[y:y+h, x:x+w])

    # Display the resulting frame
    cv2.imshow('frame', frame)

    # Exit loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and destroy windows
i = 0
for img in detects:
    cv2.imwrite(os.path.join(path, f'detect_{i}.png'), img)
    i += 1

print(len(detects))

cap.release()
cv2.destroyAllWindows()
