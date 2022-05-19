import cv2 as cv
import mediapipe as mp

"""
POSE LANDMARK VALUES

 NOSE = 0
  LEFT_EYE_INNER = 1
  LEFT_EYE = 2
  LEFT_EYE_OUTER = 3
  RIGHT_EYE_INNER = 4
  RIGHT_EYE = 5
  RIGHT_EYE_OUTER = 6
  LEFT_EAR = 7
  RIGHT_EAR = 8
  MOUTH_LEFT = 9
  MOUTH_RIGHT = 10
  LEFT_SHOULDER = 11
  RIGHT_SHOULDER = 12

"""


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)


def pose_detect(frame):
    # get pose results
    res = pose.process(frame)
    landmarklist = res.pose_landmarks # a list of landmark objects, each contains x y z
    
    
    frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)

    # draw onto frame and return it
    mp_drawing.draw_landmarks(
        frame,
        res.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    return frame
