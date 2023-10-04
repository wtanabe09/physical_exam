import sys
import math
from matplotlib import pyplot
import numpy as np
import elbow_angle

# 座標取得する際に左右反転されている．右手を取りたい場合，左手の座標を見る．
input_csv = sys.argv[1]
result_csv_path = sys.argv[2]

is_action = False
row_counter = 0
count = 0
action_number = 0
threshold = 45

result_arr = np.zeros(4) # real_time, video_time, hand_knee_distance, is_action
result_csv = np.empty((0,4))

with open(input_csv) as file:
  for line in file:
    input_arr = line.split(",")
    # 右手（左手のインデックス）
    x_doctor_right_hand = float(input_arr[(19*2)+1])
    y_doctor_right_hand = float(input_arr[(19*2)+2])
    # 右膝（左膝のインデックス）
    x_doctor_right_knee = float(input_arr[(25*2)+2])
    y_doctor_right_knee = float(input_arr[(25*2)+2])

    doctor_right_shoulder = np.array([float(input_arr[(11*2)+1]), float(input_arr[(11*2)+2])]) # 右肩（左肩インデックス）
    doctor_right_elbow = np.array([float(input_arr[(13*2)+1]), float(input_arr[(13*2)+2])]) # 右肘
    doctor_right_wrist = np.array([float(input_arr[(15*2)+1]), float(input_arr[(15*2)+2])]) # 右手首

    # 右手から右膝までの距離
    distance_hand_knee = math.sqrt((x_doctor_right_hand - x_doctor_right_knee)**2 + (y_doctor_right_hand - y_doctor_right_knee)**2)
    # print(round(row_counter/20, 1), round(distance_hand_knee, 1), end=', ')
    
    elbow = elbow_angle.calc_elbow_angle(doctor_right_shoulder, doctor_right_elbow, doctor_right_wrist)

    if is_action:
      if distance_hand_knee <= threshold:
        # hand stay
        count += 1
      if count >= 60:
        # 動作終了処理
        is_action = False
        print(f"--- end action ---")
      else:
        # 動作中処理
        if distance_hand_knee > threshold:
          count = 0
        print(f"short count:{count}, action now")
    else: # is_action false
      if distance_hand_knee > threshold:
        is_action = True
        count = 0 #2秒のカウント戻す
        action_number += 1
        # 動作開始処理
        print(f"--- start action {action_number} ---")
      else:
        print(f"stay hand")

    row_counter += 1

    # create output array for csv file
    result_arr = [input_arr[0], round(row_counter/20, 1), distance_hand_knee, elbow] # time into first col
    result_csv = np.vstack((result_csv, result_arr))

np.savetxt(result_csv_path, result_csv, delimiter = ',',fmt="%s")

