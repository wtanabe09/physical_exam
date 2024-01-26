# 入力された動画に対して姿勢推定をかけるプログラム
# input arg: python3 coordinate_output.py input_video_path output_csv_paht role_num
# example: python3 coordinate_output.py ...../202311....mp4 ....../202311......csv 1

# 必要なパッケージのインポート
import sys
import cv2
import mediapipe as mp
import numpy as np

# input_file = sys.argv[1]
# output_path = sys.argv[2]

# for test
input_file = "../kut-sample-video/01_脈1-C.mp4"
output_path = "../kut-sample-video/data_csv_files/01_脈1-C.csv"

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_holistic = mp.solutions.holistic

data_land = np.zeros((0,66)) # 0row,99column, 33 * 3

cap = cv2.VideoCapture(input_file)#load mp4 file 引数に動画ファイルのパスを渡す
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      break
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    image.flags.writeable = False
    results = holistic.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    #draw landmark
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
    
    #get coordinate
    data_land2 = np.zeros((1,0))
    
    for i in range (0,33):
        try:
          data1 = results.pose_landmarks.landmark[i].x
          data2 = results.pose_landmarks.landmark[i].y
        except AttributeError:
          data1 = np.nan
          data2 = np.nan
        keydata = np.hstack((data1,data2)).reshape(1,-1)
        data_land2 = np.hstack((data_land2,keydata)) # hstack 水平方向に結合, 0~2:landmark_id:0のx,y,z

    data_land = np.vstack((data_land,data_land2)) # vstack 縦方向に結合, 
    # 動画の描画確認
    cv2.imshow('MediaPipe Holistic', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()

np.savetxt(output_path,data_land,delimiter = ',') #csv書き込み，保存


# 参考 https://himahimaknowledge.blogspot.com/2021/12/mediapipe.html