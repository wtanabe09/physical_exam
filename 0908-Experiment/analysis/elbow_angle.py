import sys
import math
from matplotlib import pyplot
import numpy as np

input_csv = sys.argv[1] #csv ファイルセレクト
# output_csv_path = sys.argv[2]


def calc_elbow_angle(shoulder, elbow, wrist):
  elbow_to_shoulder = shoulder - elbow # ベクトル
  elbow_to_wrist = wrist - elbow # ベクトル

  dot_product = np.dot(elbow_to_shoulder, elbow_to_wrist)

  norm_elbow_to_shoulder = np.linalg.norm(elbow_to_shoulder)
  norm_elbow_to_wrist = np.linalg.norm(elbow_to_wrist)

  cos_theta = dot_product / (norm_elbow_to_shoulder * norm_elbow_to_wrist)
  angle_radians = np.arccos(np.clip(cos_theta, -1.0, 1.0))

  # ラジアンから度に変換
  angle_degrees = math.degrees(angle_radians)
  
  return 180 - angle_degrees

# with open(input_csv) as file:
#   for line in file:
#     input_arr = line.split(",")

#     doctor_right_shoulder = np.array([float(input_arr[(11*2)+1]), float(input_arr[(11*2)+2])]) # 右肩（左肩インデックス）
#     doctor_right_elbow = np.array([float(input_arr[(13*2)+1]), float(input_arr[(13*2)+2])]) # 右肘
#     doctor_right_wrist = np.array([float(input_arr[(15*2)+1]), float(input_arr[(15*2)+2])]) # 右手首

#     print(calc_elbow_angle(doctor_right_shoulder, doctor_right_elbow, doctor_right_wrist))
