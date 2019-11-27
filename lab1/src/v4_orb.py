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
    
    # Initiate STAR detector
    orb = cv2.ORB_create(nfeatures=1000)

    # find the keypoints with ORB
    kp = orb.detect(gray,None)

    # compute the descriptors with ORB
    kp, des = orb.compute(gray, kp)

    # draw only keypoints location,not size and orientation
    frame_kp = cv2.drawKeypoints(gray,kp,outImage = None, color=(0,255,0), flags=0)

    # Show video
    cv2.imshow('ORB',frame_kp)

    # Exit if "4" is pressed
    k = cv2.waitKey(1) & 0xFF
    if k == 52 : #ord 4
        #Quit
        print ('Good Bye!')
        break

#Release the Cap and Video   
cap.release()
cv2.destroyAllWindows()
