import cv2
import numpy as np

frame = cv2.imread('map.png')
img = frame
hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

lower_blue = np.array([107,92,255])
upper_blue = np.array([107,92,255])

mask = cv2.inRange(hsv, lower_blue, upper_blue)
res = cv2.bitwise_and(frame,frame, mask=mask)
mask_thresh = cv2.erode(mask,None,iterations=2)
mask_thresh = cv2.dilate(mask_thresh,None,iterations=4)
f = 0;
cv2.imshow('img',img);
cv2.imshow('mask',mask);
cv2.imshow('res',res);
cv2.imshow('normalized',mask_thresh);
cv2.waitKey(0);
dimensions = mask_thresh.shape
for i in range(dimensions[0]):
    for j in range(dimensions[1]):
        if mask_thresh[i,j] == 255:
            print("Water body is present")
            f = 1
            break
    else:
        continue
    break
if f==0:
    print("Water body is not present.")
