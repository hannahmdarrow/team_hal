import cv2 as cv
import mediapipe as mp


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)


def pose_detect(frame):
    # get pose results
    res = pose.process(frame)
    print(res)
    
    
    frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)

    # draw onto frame and return it
    mp_drawing.draw_landmarks(
        frame,
        res.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    return frame
