import cv2
import numpy as np

# Initialize webcam
cap = cv2.VideoCapture(0)

while True:
    # Read frame from webcam
    ret, frame = cap.read()
    
    # Convert BGR to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Define range of red color in HSV
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    
    # Threshold the HSV image to get only red colors
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    
    lower_red = np.array([170, 50, 50])
    upper_red = np.array([180, 255, 255])
    
    mask2 = cv2.inRange(hsv, lower_red, upper_red)
    
    # Combine masks
    mask = mask1 + mask2
    
    # Bitwise-AND mask and original image
    #res = cv2.bitwise_and(frame, frame, mask=mask)
    
    # Find contours of the red object
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Draw contours on the original frame
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)
    
    # Display the resulting frame
    cv2.imshow('Original', frame)
    #cv2.imshow('Mask', mask)
    #cv2.imshow('Result', res)
    
    # Exit loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()