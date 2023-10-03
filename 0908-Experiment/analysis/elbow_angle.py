import sys
import math
from matplotlib import pyplot
import numpy as np

input_csv = sys.argv[1] #csv ファイルセレクト
# output_csv_path = sys.argv[2]

with open(input_csv) as file:
  for line in file:
    input_arr = line.split(",")

    # 右肩（左肩インデックス）
    doctor_right_shoulder = np.array([float(input_arr[11*2]+1), float(input_arr[11*2]+2)])
    # 右肘
    doctor_right_elbow = np.array([float(input_arr[(13*2)+1]), float(input_arr[(13*2)+2])])
    # 右手首
    doctor_right_wrist = np.array([float(input_arr[(15*2)+1]), float(input_arr[(15*2)+2])])
    calc_elbow_angle(doctor_right_shoulder, doctor_right_elbow, doctor_right_wrist)


def calc_elbow_angle(shoulder, elbow, wrist):
  elbow_to_shoulder = shoulder - elbow # ベクトル
  elbow_to_wrist = wrist - elbow # ベクトル