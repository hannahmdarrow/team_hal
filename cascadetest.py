from __future__ import print_function
from cmath import pi
import cv2 as cv
import argparse
import keyboard

baselineValue = (0,0,0,0)
currentValue = (0,0,0,0)


def detectAndDisplay(frame, baseline, currentValue, face_cascade):#main camera loop function
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)
    
    #-- Detect faces
    faces = face_cascade.detectMultiScale(frame_gray)
    
    for (x,y,w,h) in faces:
        center = (x + w//2, y + h//2)
        frame = cv.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)
        faceROI = frame_gray[y:y+h,x:x+w]
        currentValue = (x,y,h,w)
      
    upperHigh = 0 #establishing too far threshold
    upperLow = 0#too close threshold
    baselineVal = 0

    if (len(baseline) > 3):
        
        for z in baseline["baselineValue"]:#turning baseline tuple into a numerical value
            baselineVal += z

        if baselineVal != 0:
            for x in currentValue:
                upperHigh += x
                upperLow += x

            upperHigh += upperHigh*.05
            upperLow -= upperLow*.05
        
            if upperHigh < baselineVal:
                print("Too FAR!!")
                frame = cv.putText(frame, "Too FAR!!", (30,70), cv.FONT_HERSHEY_DUPLEX, 1, (255,255,255), lineType=cv.LINE_AA, thickness=2)
                frame = cv.putText(frame, "Too FAR!!", (30,70), cv.FONT_HERSHEY_DUPLEX, 1, (0,255,0), )
            if upperLow > baselineVal:
                print("TOO Close!!")
                frame = cv.putText(frame, "Too CLOSE!!", (30,70), cv.FONT_HERSHEY_DUPLEX, 1, (255,255,255), lineType=cv.LINE_AA, thickness=2)
                frame = cv.putText(frame, "Too CLOSE!!", (30,70), cv.FONT_HERSHEY_DUPLEX, 1, (0,255,0), )
        
        print(x+y+w+h, baselineVal)


    #cv.imshow('Capture - Face detection', frame) # this is done in main
    return currentValue, abs(1 - (x+y+w+h)/(baselineVal))
