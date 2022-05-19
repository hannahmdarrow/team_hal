from __future__ import print_function
import cv2 as cv
import argparse
import keyboard

baselineValue = (0,0,0,0)
currentValue = (0,0,0,0)
def comparingBaseline(baselineValue, currentValue):
    x = currentValue[0]
    y = currentValue[1]
    w = currentValue[2]
    h = currentValue[3]

    upperHigh = 0 #establishing too far threshold
    upperLow = 0#too close threshold
    baselineVal = 0
    currentVal = 0#what is coming live from the feed
    
    for z in baselineValue:#turning baseline tuple into a numerical value
        baselineVal += z

    if baselineVal != 0:
        for x in currentValue:
            upperHigh += x
            upperLow += x

        upperHigh += upperHigh*.01
        upperLow -= upperLow*.02
    
        if upperHigh < baselineVal:
            print("Too FAR!!")
        if upperLow > baselineVal:
            print("TOO Close!!")


def detectAndDisplay(frame, baselineValue, currentValue, face_cascade):#main camera loop function
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)
    
    #-- Detect faces
    faces = face_cascade.detectMultiScale(frame_gray)
    
    for (x,y,w,h) in faces:
        center = (x + w//2, y + h//2)
        frame = cv.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)
        faceROI = frame_gray[y:y+h,x:x+w]
        currentValue = (x,y,h,w)
        
    #cv.imshow('Capture - Face detection', frame) # this is done in main
    return None, baselineValue, currentValue
