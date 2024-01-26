# 特徴量を計算するプログラム，analysis2.pyから呼び出される．
# 内積，ユーグリッド距離，x座標距離，最大値3つの平均を取る

import math
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


def distance(point_a, point_b): # ユーグリッド距離
  return math.sqrt((point_a[0] - point_b[0])**2 + (point_a[1] - point_b[1])**2)

def x_distance(point_a, point_b): # x座標の距離（差分）引数[0:x座標，1:y座標]
  return point_a[0] - point_b[0]

def y_distance(point_a, point_b): # y座標の距離（差分）引数[0:x座標，1:y座標]
  return point_a[1] - point_b[1]


# 正規化に使用する，肩から腰までのyの距離の最大値3つの平均値を返す．距離の特徴量/肩から腰までのyの距離
def max_a_to_b(input_csv, index_a, index_b):
  max_ab_arr = []
  with open(input_csv) as file:
    next(file)
    for line in file:
      input_arr = line.split(",")
      index_a_y =  float(input_arr[(index_a*2)+2]) # 1/4時点 肩を想定
      index_b_y = float(input_arr[(index_b*2)+2]) # 1/4時点 腰を想定
      max_ab_arr.append(index_b_y - index_a_y) # bの方が大きい値を書く

  largest3 = heapq.nlargest(3, max_ab_arr)
  max_ab = sum(largest3) / 3 #大きい三つの平均
  return max_ab
