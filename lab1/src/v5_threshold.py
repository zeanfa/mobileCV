import numpy as np
import cv2
from sklearn.cluster import KMeans

print('Press 4 to Quit the Application\n')

#Open Default Camera
cap = cv2.VideoCapture(0)

while(cap.isOpened()):
    #Take each Frame
    ret, frame = cap.read()
    
    #Flip Video vertically (180 Degrees)
    frame = cv2.flip(frame, 180)

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Denoise 
    gray = cv2.GaussianBlur(gray,(3,3),0)

    # Adaptive thresholding
    blockSize = 7
    th2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blockSize, 2)

    # Show video
    cv2.imshow('Cam', frame)
    cv2.imshow('Adaptive threshold', th2)

    # Exit if "4" is pressed
    k = cv2.waitKey(1) & 0xFF
    if k == 52 : #ord 4
        #Quit
        print ('Good Bye!')
        break

#Release the Cap and Video   
cap.release()
cv2.destroyAllWindows()
