from __future__ import print_function
import cv2 as cv
import argparse
import keyboard

def comparingBaseline():
    pass


def detectAndDisplay(frame, baselineValue):#main camera loop function
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)
    
    #-- Detect faces
    faces = face_cascade.detectMultiScale(frame_gray)
    
    for (x,y,w,h) in faces:
        center = (x + w//2, y + h//2)
        frame = cv.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)
        faceROI = frame_gray[y:y+h,x:x+w]

        try:  # used try so that if user pressed other than the given key error will not be shown
            if keyboard.is_pressed('D'):  # if key 'q' is pressed, capture baseline
                print('Capturing Baseline Value')
                baselineValue = (x,y,h,w)
                print(baselineValue)
                
                break  # finishing the loop
        except:
            break  # if user pressed a key other than the given key the loop will break
    cv.imshow('Capture - Face detection', frame)
    return None, baselineValue

