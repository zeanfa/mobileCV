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

    # Get frame size
    width, height, channels = frame.shape

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Denoise 
    gray = cv2.GaussianBlur(gray,(3,3),0)

    # Histogram
    histSize = 4
    histRange = (0, 256) # the upper boundary is exclusive
    accumulate = False
    hist = cv2.calcHist([gray[60:420,:]], [0], None, [histSize], histRange, accumulate=accumulate)
    hist_w = 512
    hist_h = 480
    bin_w = int(round(hist_w/(histSize-1)))
    histImage = np.zeros((hist_h, hist_w, 1), dtype=np.uint8)
    cv2.normalize(hist, hist, alpha=0, beta=hist_h, norm_type=cv2.NORM_MINMAX)
    for i in range(1, histSize):
        cv2.line(histImage, ( bin_w*(i-1), hist_h - int(hist[i-1].round()) ),
            ( bin_w*(i), hist_h - int(hist[i].round()) ),
            ( 255, 255, 255), thickness=2)
    
    # Show video
    cv2.imshow('Histogram',histImage)
    cv2.imshow('Cam',gray)

    # Exit if "4" is pressed
    k = cv2.waitKey(1) & 0xFF
    if k == 52 : #ord 4
        #Quit
        print ('Good Bye!')
        break

#Release the Cap and Video   
cap.release()
cv2.destroyAllWindows()
