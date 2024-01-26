# 入力された動画に対して姿勢推定をかけるプログラム
# 医者か患者の役割(1or2)を指定し，指定した役割の座標が取得できる
# input arg: python3 coordinate_output.py input_video_path output_csv_paht role_num
# example: python3 coordinate_output.py ...../202311....mp4 ....../202311......csv 1

# 必要なパッケージのインポート
import sys
import os
import cv2
import mediapipe as mp
import numpy as np

input_file = sys.argv[1] # .mp4ファイル
output_csv_path = sys.argv[2] # .csvファイル
output_video_path = sys.argv[3] #.mp4
role_num = sys.argv[4] # 1 or 2

# for test
# input_file = "../kut-sample-video/01_脈1-C.mp4"
# output_csv_path = "../kut-sample-video/data_csv_files/01_脈1-C-2.csv"
# output_video_path = "../kut-sample-video/data_video_files/01_脈1-C-2.mp4"
# role_num = "2"

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_holistic = mp.solutions.holistic

# prepare data array for csv
data_land = np.zeros((0,66)) # 0row,99column, 33 * 2
# stream mp4 file
cap = cv2.VideoCapture(input_file) # load mp4 file 引数に動画ファイルのパスを渡す
im_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
im_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v') # ファイル形式(ここではmp4)
size = (im_width, im_height)
writer = cv2.VideoWriter(output_video_path, fmt, fps, size) # ライター作成

with mp_holistic.Holistic(
    min_detection_confidence=0.8,
    min_tracking_confidence=0.5) as holistic:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      break
    
    # モザイク処理
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # 1frame の画像OpenCV用にカラーの方式を変換
    if role_num == "1":
      # movie edit for doctor
      xy1 = (int(im_width*0.6), int(im_height*0.1))
      xy2 = (int(im_width*0.8), int(im_height*0.9))
    elif role_num == "2":
      # movie edit for patient
      xy1 = (int(im_width*0.2), int(im_height*0.1))
      xy2 = (int(im_width*0.4), int(im_height*0.9))

    image = cv2.rectangle(image, xy1, xy2, (0, 255, 0), thickness=-1)

    image.flags.writeable = False
    results = holistic.process(image) # holistic.process のなかに座標データなど閉じ込められている．

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    #draw landmark
    mp_drawing.draw_landmarks(
        image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
    
    writer.write(image)
    
    #get coordinate
    data_land2 = np.zeros((1,0))
    for i in range (0,33):
        try:
          data1 = results.pose_landmarks.landmark[i].x * im_width
          data2 = results.pose_landmarks.landmark[i].y * im_height
        except AttributeError:
          data1 = np.nan
          data2 = np.nan
        keydata = np.hstack((data1,data2)).reshape(1,-1)
        data_land2 = np.hstack((data_land2,keydata)) # hstack 水平方向に結合, 0~2:landmark_id:0のx,y,z

    data_land = np.vstack((data_land, data_land2)) # vstack 縦方向に結合,

    # play movie
    # cv2.imshow('MediaPipe Holistic', image)
    # if cv2.waitKey(5) & 0xFF == 27:
    #   break

cap.release()
writer.release()
np.savetxt(output_csv_path,data_land,delimiter = ',', fmt='%d') #csv書き込み，保存