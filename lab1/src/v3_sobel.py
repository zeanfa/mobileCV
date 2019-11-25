import numpy as np
import cv2

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

    # Sobel filter
    h = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)
    v = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
    sobel = cv2.addWeighted(h, 0.5, v, 0.5, 0)
    thd_abs = cv2.convertScaleAbs(sobel, alpha=3)

    # Show video
    cv2.imshow('Detect Boundaries',thd_abs)
    cv2.imshow('Webcam',frame)

    # Exit if "4" is pressed
    k = cv2.waitKey(1) & 0xFF
    if k == 52 : #ord 4
        #Quit
        print ('Good Bye!')
        break

#Release the Cap and Video   
cap.release()
cv2.destroyAllWindows()
