# example: python3 coordinate_output.py ...../202311....mp4 ....../202311......mp4

# 必要なパッケージのインポート
import sys
import os
import cv2
import mediapipe as mp
import numpy as np

input_file = sys.argv[1]
output_path = sys.argv[2]

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_holistic = mp.solutions.holistic

data_land = np.zeros((0,99)) # 0row,99column, 33 * 3
# stream mp4 file
cap = cv2.VideoCapture(input_file)#load mp4 file 引数に動画ファイルのパスを渡す
with mp_holistic.Holistic(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as holistic:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      break

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    image.flags.writeable = False
    results = holistic.process(image)
    # holistic.process のなかに座標データなど閉じ込められている．

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    #draw landmark
    # mp_drawing.draw_landmarks(
    #     image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
    # mp_drawing.draw_landmarks(
    #     image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
    # mp_drawing.draw_landmarks(
    #     image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
    
    #get coordinate
    data_land2 = np.zeros((1,3))
    
    for i in range (0,33):
        try:
          data1 = results.pose_landmarks.landmark[i].x
          data2 = results.pose_landmarks.landmark[i].y
          # data3 = results.pose_landmarks.landmark[i].z
        except AttributeError:
          data1 = np.nan
          data2 = np.nan
          # data3 = np.nan
        # keydata = np.hstack((data1,data2,data3)).reshape(1,-1)
        keydata = np.hstack((data1,data2)).reshape(1,-1)
        data_land2 = np.hstack((data_land2,keydata)) # hstack 水平方向に結合, 0~2:landmark_id:0のx,y,z

    data_land2 = data_land2[:,3:] # 全行，３列目から最後まで
    data_land = np.vstack((data_land,data_land2)) # vstack 縦方向に結合, 
    # cv2.imshow('MediaPipe Holistic', image)
    # if cv2.waitKey(5) & 0xFF == 27:
    #   break
cap.release()

np.savetxt(output_path,data_land,delimiter = ',') #csv書き込み，保存


# 参考 https://himahimaknowledge.blogspot.com/2021/12/mediapipe.html