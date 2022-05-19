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

    #x +=x*.10
    #y +=y*.10
    #w +=w*.10
    #h +=h*.10
    upperHigh = 0
    currentVal = 0
    for x in currentValue:
        upperHigh += x

    for y in baselineValue:
        currentVal += y

    upperHigh += upperHigh*.01
    
    if upperHigh < currentVal:
        print("Too FAR!!")

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
        try:  # used try so that if user pressed other than the given key error will not be shown
            if keyboard.is_pressed('D'):  # if key 'q' is pressed, capture baseline
                print('Capturing Baseline Value')
                baselineValue = (x,y,h,w)
                #print(baselineValue)
                break  # finishing the loop
        except:
            break  # if user pressed a key other than the given key the loop will break
    cv.imshow('Capture - Face detection', frame)
    return None, baselineValue, currentValue
