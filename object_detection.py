# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 00:29:21 2019

@author: karad
"""

import cv2
import numpy as np

cap = cv2.VideoCapture(1)
obj = cv2.imread("telefon.jpg",0)

while True:
    ret, frame = cap.read()
   
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    w,h = obj.shape
    res = cv2.matchTemplate(gray,obj,cv2.TM_CCOEFF_NORMED)
    tresh = 0.8
    loc = np.where(res>tresh)
    for n in zip(*loc[::-1]):
        cv2.rectangle(frame,n,(n[0]+h,n[1]+w),(0,255,0),2)
        
    cv2.imshow("frame",frame)
    
    key = cv2.waitKey(10)
    if key == 27:
        break
    
cap.release()
cv2.destroyAllWindows()
    
    