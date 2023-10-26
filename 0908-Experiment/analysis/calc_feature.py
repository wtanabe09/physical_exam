import sys
import math
from matplotlib import pyplot
import numpy as np
import heapq

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
  return math.sqrt((point_a[0] - point_b[0])**2 + (point_a[1] - point_b[1])**2)

def x_distance(point_a, point_b):
  return point_a[0] - point_b[0]

def max_a_to_b(input_csv, index_a, index_b):
  shoulder_hip_arr = []
  with open(input_csv) as file:
    for line in file:
      input_arr = line.split(",")
      shoulder_y =  float(input_arr[(index_a*2)+2])
      hip_y = float(input_arr[(index_b*2)+2])
      shoulder_hip_arr.append(hip_y - shoulder_y)

  largest = heapq.nlargest(3, shoulder_hip_arr)
  max_shoulder_hip = sum(largest) / 3 #大きい三つの平均
  return max_shoulder_hip
