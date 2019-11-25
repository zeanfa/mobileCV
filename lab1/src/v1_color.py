import numpy as np
import cv2

print('Press 4 to Quit the Application\n')

upper = [0,0,0]
#Find HSV Green Value 
green = np.uint8([[[0,255,0]]])
hsv_green = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)
print(hsv_green)

#Found Upper Value
for i in hsv_green:
    for j in i:
        upper[0] += (j[0])
        upper[1] += (j[1])
        upper[2] += (j[2])
    for i in range (len(upper)):
        if upper[i] == 255:
            pass
        else:
            upper[i] += 20
#Found Lower Value
lower = upper.copy()
for j in range (len(lower)):
    if lower[j] == 255:
        lower[j] = 10
    else:
        lower[j] -= 40

#Open Default Camera
cap = cv2.VideoCapture(0)

while(cap.isOpened()):
    #Take each Frame
    ret, frame = cap.read()
    
    #Flip Video vertically (180 Degrees)
    frame = cv2.flip(frame, 180)

    #Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Get frame size
    width, height, channels = frame.shape

    rect_size = 50

    # Start coordinate, here (5, 5) 
    # represents the top left corner of rectangle 
    start_point = (int(height/2-rect_size/2), int(width/2-rect_size/2))
      
    # Ending coordinate, here (220, 220) 
    # represents the bottom right corner of rectangle 
    end_point = (int(height/2+rect_size/2), int(width/2+rect_size/2))

    # font 
    font = cv2.FONT_HERSHEY_SIMPLEX 
      
    # org 
    org = end_point
      
    # fontScale 
    fontScale = 0.7
      
    # Blue color in BGR 
    color = (255, 0, 0) 
      
    # Line thickness of 2 px 
    thickness = 1
      
    # Using cv2.rectangle() method 
    # Draw a rectangle with blue line borders of thickness of 2 px 
    rect = cv2.rectangle(frame, start_point, end_point, color, thickness)
    #print(rect.shape)

    # find average hue
    rect_hsv = hsv[int(width/2-rect_size/2):int(width/2+rect_size/2),int(height/2-rect_size/2):int(height/2+rect_size/2),:]
    #Define Range of Green Color in HSV
    upper_green = np.array(upper)
    lower_green = np.array(lower)
    # Threshold the HSV Image to Get only Green Color
    mask = cv2.inRange(rect_hsv, lower_green, upper_green)

    true = np.count_nonzero(mask)/(rect_size*rect_size)
    
    av_hue = np.average(rect_hsv[:,:,0])
    av_sat = np.average(rect_hsv[:,:,1])
    av_val = np.average(rect_hsv[:,:,2])

    average = [int(av_hue),int(av_sat),int(av_val)]
    text = cv2.putText(rect, str(average) + " " + str(true), (10,50), font,  
                           fontScale, color, thickness, cv2.LINE_AA)

    if true>0.9:
    # Using cv2.putText() method 
        text = cv2.putText(rect, ' greeny ', org, font,  
                           fontScale, color, thickness, cv2.LINE_AA)
    else:
    # Using cv2.putText() method 
        text = cv2.putText(rect, ' not greeny ', org, font,  
                           fontScale, color, thickness, cv2.LINE_AA) 

    # Show video
    cv2.imshow('Frame',rect)

    # Exit if "4" is pressed
    k = cv2.waitKey(1) & 0xFF
    if k == 52 : #ord 4
        #Quit
        print ('Good Bye!')
        break

#Release the Cap and Video   
cap.release()
cv2.destroyAllWindows()
