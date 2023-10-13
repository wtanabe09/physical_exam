# 実行例: python3 analysis.py data_csv_files/20230908111226366962_1.csv result_files/20230908111226366962_1.csv
# 座標取得する際に左右反転されている．右手の座標を見たい場合，左手の座標を見る．

import sys
import os
import math
import numpy as np
import calc_feature

input_csv = sys.argv[1]
result_csv_path = sys.argv[2]
base_name = os.path.splitext(os.path.basename(input_csv))[0]


with open(input_csv) as file:
  bool_action_now = False
  row_counter = 0
  short_distance_count = 0
  action_number = 0
  threshold = 45
  result_arr = np.zeros(4) # real_time, video_time, hand_knee_distance, is_action
  result_csv = np.empty((0,4))

  for line in file:
    input_arr = line.split(",")
    # 右手（左手のインデックス）
    right_hand_doctor = np.array([float(input_arr[(19*2)+1]), float(input_arr[(19*2)+2])])
    # 右膝（左膝のインデックス）
    right_knee_doctor = np.array([float(input_arr[(25*2)+1]), float(input_arr[(25*2)+2])])
    # 医者の右肩，右肘，右手首
    right_shoulder_doctor = np.array([float(input_arr[(11*2)+1]), float(input_arr[(11*2)+2])]) # 右肩（左肩インデックス）
    right_elbow_doctor = np.array([float(input_arr[(13*2)+1]), float(input_arr[(13*2)+2])]) # 右肘
    right_wrist_doctor = np.array([float(input_arr[(15*2)+1]), float(input_arr[(15*2)+2])]) # 右手首

    hand_knee_distance = calc_feature.distance(right_hand_doctor, right_knee_doctor) # 計算：右手から右膝までの距離
    elbow_angle = calc_feature.inner_product(right_shoulder_doctor, right_elbow_doctor, right_wrist_doctor) # 計算：肘角度

    if bool_action_now: # 動作中
      if hand_knee_distance > threshold: # 閾値より大きいなら動作中，何もしない．
        short_distance_count = 0
      else: # 閾値以下なら手を膝に置いている．以下で膝に置いている時間が３秒以上続いているか確認する．
        short_distance_count += 1
        if short_distance_count >= 60: # 閾値以下 3秒以上続いたら動作終了処理
          bool_action_now = False
          # print(f"--- end action ---")
        else: # 動作継続
          pass
          # print(f"action now, short count:{short_distance_count}")

    else: # Not 動作
      if hand_knee_distance > threshold: # 手が膝から離れたら動作開始
        bool_action_now = True
        short_distance_count = 0
        action_number += 1
        # print(f"--- start action {action_number} ---")
      else: # 手が膝から離れていなければそのまま
        pass
        # print(f"stay hand, short count:{short_distance_count}")

    row_counter += 1
    
    # create output array for csv file
    result_arr = [round(row_counter/20, 2), bool_action_now, hand_knee_distance, elbow_angle] # 一列目：動画の時間
    result_csv = np.vstack((result_csv, result_arr))

np.savetxt(result_csv_path, result_csv, delimiter = ',',fmt="%s")

