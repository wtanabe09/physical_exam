#　!! 編集中 ¡¡ PoseLandmarikのモデルをつかって，複数人表示したい．
# example: python3 coordinate_output.py ...../202311....mp4 ....../202311......mp4

# 必要なパッケージのインポート
import sys
import cv2
import mediapipe as mp
import numpy as np

from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2


# input_video = sys.argv[1]
# output_csv_path = sys.argv[2]

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_holistic = mp.solutions.holistic

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

# data_land = np.zeros((0,66)) # 0row,99column, 33 * 3
# stream mp4 file
# cap = cv2.VideoCapture(input_video)#load mp4 file 引数に動画ファイルのパスを渡す

def draw_landmarks_on_image(rgb_image, detection_result):
  pose_landmarks_list = detection_result.pose_landmarks
  annotated_image = np.copy(rgb_image)

  # Loop through the detected poses to visualize.
  for idx in range(len(pose_landmarks_list)):
    pose_landmarks = pose_landmarks_list[idx]

    # Draw the pose landmarks.
    pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
    pose_landmarks_proto.landmark.extend([
      landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks
    ])
    solutions.drawing_utils.draw_landmarks(
      annotated_image,
      pose_landmarks_proto,
      solutions.pose.POSE_CONNECTIONS,
      solutions.drawing_styles.get_default_pose_landmarks_style())
  return annotated_image

options = PoseLandmarkerOptions(
    base_options=BaseOptions,
    running_mode=VisionRunningMode.IMAGE,
    num_poses=2)

with PoseLandmarker.create_from_options(options) as landmarker:

    # Load the input image from an image file.
    mp_image = mp.Image.create_from_file('/path/to/image')

    # STEP 4: Detect pose landmarks from the input image.
    detection_result = landmarker.detect(mp_image)

# STEP 5: Process the detection result. In this case, visualize it.
# annotated_image = mp_drawing.draw_landmarks(mp_image.numpy_view(), detection_result)
# cv2.imshow(cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))