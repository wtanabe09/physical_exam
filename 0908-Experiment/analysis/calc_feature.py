import sys
import math
from matplotlib import pyplot
import numpy as np

# input_csv = sys.argv[1] #csv ファイルセレクト
# output_csv_path = sys.argv[2]

def inner_product(point_a,  point_o, point_b): # ３点のx,y座標の配列
  oa_bector = point_a - point_o # o→a ベクトル
  ob_bector = point_b - point_o # o→b ベクトル

  dot_product = np.dot(oa_bector, ob_bector)

  norm_oa = np.linalg.norm(oa_bector)
  norm_ob = np.linalg.norm(ob_bector)

  cos_theta = dot_product / (norm_oa * norm_ob)
  angle_radians = np.arccos(np.clip(cos_theta, -1.0, 1.0))

  angle_degrees = math.degrees(angle_radians) # ラジアンから度に変換
  return 180 - angle_degrees


def distance(point_a, point_b):
  distance = math.sqrt((point_a[0] - point_b[0])**2 + (point_a[1] - point_b[1])**2)
  return distance


# with open(input_csv) as file:
#   for line in file:
#     input_arr = line.split(",")

#     doctor_right_shoulder = np.array([float(input_arr[(11*2)+1]), float(input_arr[(11*2)+2])]) # 右肩（左肩インデックス）
#     doctor_right_elbow = np.array([float(input_arr[(13*2)+1]), float(input_arr[(13*2)+2])]) # 右肘
#     doctor_right_wrist = np.array([float(input_arr[(15*2)+1]), float(input_arr[(15*2)+2])]) # 右手首

#     print(calc_elbow_angle(doctor_right_shoulder, doctor_right_elbow, doctor_right_wrist))
