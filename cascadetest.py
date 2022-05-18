from __future__ import print_function
import cv2 as cv
import argparse
import keyboard

baselineValue = (0,0,0,0)

def comparingBaseline():
    


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

parser = argparse.ArgumentParser(description='Code for Cascade Classifier tutorial.')
parser.add_argument('--face_cascade', help='Path to face cascade.', default='haarcascade_frontalface_alt.xml')
parser.add_argument('--camera', help='Camera divide number.', type=int, default=0)
args = parser.parse_args()
face_cascade_name = args.face_cascade
face_cascade = cv.CascadeClassifier()

#-- 1. Load the cascades
if not face_cascade.load(cv.samples.findFile(face_cascade_name)):
    print('--(!)Error loading face cascade')
    exit(0)
camera_device = args.camera

#-- 2. Read the video stream
cap = cv.VideoCapture(camera_device)
if not cap.isOpened:
    print('--(!)Error opening video capture')
    exit(0)
while True:
    ret, frame = cap.read()
    if frame is None:
        print('--(!) No captured frame -- Break!')
        break
    _, baselineValue = detectAndDisplay(frame, baselineValue)
    if cv.waitKey(1) & 0xFF == ord('q'):#program closes when q is pressed.
        break
cv.destroyAllWindows()
