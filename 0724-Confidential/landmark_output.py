# ランドマーク映像の表示, 保存．
# coordinate_outputでcsv出力, landmark_outpuで動画出力, 役割分担のため用意．
# 現在はcoordinate_outputに統合済み.こちらは映像の保存のみ．(csv出力なし)
import sys
import cv2
import mediapipe as mp
import numpy as np
import datetime

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# For vodep input:
file_base = sys.argv[1]
input_file = './crop/'+file_base+'-C.mp4'
cap = cv2.VideoCapture(input_file)

video_fps = cap.get(cv2.CAP_PROP_FPS)
video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))    
video_hight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
size = (video_width, video_hight)

fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
writer = cv2.VideoWriter('./landmark_video/'+file_base+'-C_land.mp4', fmt, video_fps, size)

with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,) as pose:
  while cap.isOpened():
    success, image = cap.read()
    if not success: 
      print("Ignoring empty camera frame.")
      break

    # mediapipeに左を読み込ませる
    if (cap.get(cv2.CAP_PROP_POS_FRAMES) <= 1):
      print(cap.get(cv2.CAP_PROP_POS_FRAMES))
      cv2.rectangle(image, (150, 0), (video_width, video_hight), (0, 255, 0), thickness=-1)
    
    # 現在時刻挿入
    dt_now = datetime.datetime.now()
    cv2.putText(image, f'{dt_now}', (0, 20), \
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), thickness=2)
    
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
    
    # cv2.imshow('MediaPipe Pose', image)
    writer.write(image)
    # if cv2.waitKey(5) & 0xFF == ord('q'):
    #   break
cap.release()
writer.release()
cv2.destroyAllWindows()
