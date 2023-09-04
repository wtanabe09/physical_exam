# 骨格点の座標を出力し, CSVファイルに保存するプログラム
import sys
import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# file path:
file_base = sys.argv[1]
input_file = './crop/'+file_base+'-C.mp4'
output_csv_path = './point_csv/'+file_base+'-C.csv'
output_land_path = './landmark_video/'+file_base+'-C_land.mp4'

# For video read and write
cap = cv2.VideoCapture(input_file)
video_fps = cap.get(cv2.CAP_PROP_FPS)
video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))    
video_hight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
size = (video_width, video_hight)
fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
writer = cv2.VideoWriter(output_land_path, fmt, video_fps, size)

data_land = np.zeros((0,66)) # For csv file, (0row,66column, 33 * 2)
error_count = 0
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
  while cap.isOpened():
    success, image = cap.read()
    now_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
    if not success:
      print("Ignoring empty camera frame.")
      break

    # mediapipeに左を読み込ませる
    # if (cap.get(cv2.CAP_PROP_POS_FRAMES) <= 1):
    cv2.rectangle(image, (190, 0), (video_width, video_hight), (0, 255, 0), thickness=-1)

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
    
    writer.write(image)
    
    data_land2 = np.zeros((1,3))
    for i in range (0,33):
        try:
            data1 = results.pose_landmarks.landmark[i].x
            data2 = results.pose_landmarks.landmark[i].y
        except AttributeError as e:
            data1 = 1 # NoneTypeの場合1を挿入する
            data2 = 1
            if i == 1:
              print(f"attribute error: {e}, frame: {now_frame}, point: {i}")
              error_count += 1
        keydata = np.hstack((data1,data2)).reshape(1,-1)
        data_land2 = np.hstack((data_land2,keydata)) # hstack 水平方向に結合, 0~2:landmark_id:0のx,y,z
    data_land2 = data_land2[:,3:] # 全行，
    data_land = np.vstack((data_land,data_land2)) # vstack 縦方向に結合, 

cap.release()
writer.release()

print(error_count)
np.savetxt(output_csv_path,data_land,delimiter = ',') #csv書き込み，保存