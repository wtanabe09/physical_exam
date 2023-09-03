# ランドマーク映像の表示と, CSVファイルの書き込み保存を行うプログラム

import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

data_land = np.zeros((0,66)) # 0row,99column, 33 * 3
# For webcam input:
cap = cv2.VideoCapture('c_0015_通し-C.mp4')
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,) as pose:
  while cap.isOpened():
    success, image = cap.read()
    if not success: 
      print("Ignoring empty camera frame.")
      break
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    
    data_land2 = np.zeros((1,3))
    for i in range (0,33):
        try:
            data1 = results.pose_landmarks.landmark[i].x
            data2 = results.pose_landmarks.landmark[i].y
            # data3 = results.pose_landmarks.landmark[i].z
        except AttributeError as e:
            data1 = 0
            data2 = 0
            print(f"attribute error: {e}")
        keydata = np.hstack((data1,data2)).reshape(1,-1)
        data_land2 = np.hstack((data_land2,keydata)) # hstack 水平方向に結合, 0~2:landmark_id:0のx,y,z
    data_land2 = data_land2[:,3:] # 全行，
    data_land = np.vstack((data_land,data_land2)) # vstack 縦方向に結合, 

    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Pose', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()

np.savetxt('./c_0015_num2_keypoint_results.csv',data_land,delimiter = ',') #csv書き込み，保存