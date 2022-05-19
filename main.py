from __future__ import print_function
import cv2 as cv
import argparse
import keyboard
import tkinter as tk
from cascadetest import detectAndDisplay
from cascadetest import comparingBaseline
from posetracking import pose_detect

window = tk.Tk()
greeting = tk.Label(text="Sit up straight")
greeting.pack()
button = tk.Button(
    text="Ready",
    width=20,
    height=3,
    bg="light blue",
    fg="black",
    command=window.destroy
)
button.pack()
window.mainloop()

# set up for face detection
baselineValue = (0,0,0,0)
currentValue = (0,0,0,0)
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

    # mark image as read only
    frame.flags.writeable = False

    # call face detection
    _, baselineValue, currentValue = detectAndDisplay(frame, baselineValue, currentValue, face_cascade)
    comparingBaseline(baselineValue, currentValue)

    # call pose detectio
    _ = pose_detect(frame)


    if cv.waitKey(1) & 0xFF == ord('q'):#program closes when q is pressed.
        break
cv.destroyAllWindows()
quit()
