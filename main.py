from __future__ import print_function
import cv2 as cv
import argparse
from cv2 import FONT_HERSHEY_DUPLEX
import keyboard
from cascadetest import detectAndDisplay
from cascadetest import comparingBaseline
from posetracking import pose_detect, pose_values
import tkinter as tk
from collections import deque

# Create a GUI window
window = tk.Tk()
greeting = tk.Label(text="Sit up straight", width=20, height=3, bg="black", fg="light blue")
greeting.pack()
# Ready button
button = tk.Button(
    text="Ready",
    width=20,
    height=3,
    bg="light blue",
    fg="black",
    # Close the window when the ready button is pushed)
    command=window.destroy
).pack()
window.mainloop()


# variables
# dictionary that stores baseline values
baseline = {}
baselineValue = (0,0,0,0)
currentValue = (0,0,0,0)

deviation = 0
queuelen = 10
scores = deque(maxlen=queuelen)

good, bad = 0, 0

parser = argparse.ArgumentParser(description='posture.ly')
parser.add_argument('--face_cascade', help='Path to face cascade.', default='haarcascade_frontalface_alt.xml')
parser.add_argument('--camera', help='Camera divide number.', type=int, default=0)
args = parser.parse_args()
face_cascade_name = args.face_cascade
face_cascade = cv.CascadeClassifier()

#-- 1. Load the cascades
if not face_cascade.load(cv.samples.findFile(face_cascade_name)):
    print('--(!)Error loading face cascade')
    exit(0)

camera_device = args.camera # should be 0 to be device default?

#-- 2. Read the video stream
cap = cv.VideoCapture(camera_device)
if not cap.isOpened:
    print('--(!)Error opening video capture')
    exit(0)



while True:
    # frame is a 2d array of rgb values -> breakdown of the iamge
    ret, frame = cap.read()
    #print(frame)
    if frame is None:
        print('--(!) No captured frame -- Break!')
        break

    # if baseline has been captured
    if (len(baseline) > 3):
        # call face detection
        currentValue = detectAndDisplay(frame, baseline, currentValue, face_cascade)
        face_deviation = comparingBaseline(baseline["baselineValue"], currentValue)
        print(face_deviation)

        # call pose detect
        frame, pose_deviation = pose_detect(frame, baseline)
        total_deviation = face_deviation + pose_deviation
        print("HWOOWOO", face_deviation, pose_deviation)
        scores.append(total_deviation)
        print(scores)

        # check for deviation
        if sum(scores) > queuelen * 3:
            frame = cv.putText(cv.flip(frame, 1), "Bad", (30,30), cv.FONT_HERSHEY_DUPLEX, 1, (0,0,255))
            bad += 1
        else:
            frame = cv.putText(cv.flip(frame, 1), "Good", (30,30), cv.FONT_HERSHEY_DUPLEX, 1, (0,255,0))
            good += 1
    else:
        frame = cv.flip(frame, 1)

    cv.imshow('MediaPipe Pose', frame)

    # get baseline values
    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('D'):  # if key 'D' is pressed, capture baseline
            print('Capturing Baseline Value')
            baseline["baselineValue"] = detectAndDisplay(frame, baseline, currentValue, face_cascade)

            xs, ys, zs, s = pose_values(frame)
            baseline["xslant"] = xs
            baseline["yslant"] = ys
            baseline["zslant"] = zs
            baseline["slouch"] = s
    except:
        pass  # if user pressed a key other than the given key the loop will break


    if cv.waitKey(1) & 0xFF == ord('q'):#program closes when q is pressed.
        print("Percentage good:", good/bad)
        break
cv.destroyAllWindows()
quit()
