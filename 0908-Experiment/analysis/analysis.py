import sys
import math
from matplotlib import pyplot
import numpy as np

# 座標取得する際に左右反転されている．右手を取りたい場合，左手の座標を見る．
input_file = sys.argv[1] #csv ファイルセレクト
output_file_path = sys.argv[2]

is_action = False
row_counter = 0
count = 0
action_number = 0
threshold = 45

output_arr = np.zeros(4)
output_csv = np.empty((0,4))

with open(input_file) as file:
  for line in file:
    input_arr = line.split(",")
    right_hand_x = float(input_arr[(19*2)+1]) # 左手のインデックス（右手）
    right_hand_y = float(input_arr[(19*2)+2])
    right_knee_x = float(input_arr[(25*2)+2]) # 左膝のインデックス（右膝）
    right_knee_y = float(input_arr[(25*2)+2])

    # 右手から右膝までの距離
    distance_hand_knee = math.sqrt((right_hand_x - right_knee_x)**2 + (right_hand_y - right_knee_y)**2)
    print(round(row_counter/20, 1), round(distance_hand_knee, 1), end=', ')
    
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
    output_arr[0] = input_arr[0] # time into first col
    output_arr[1] = round(row_counter/20, 1) # video seconds into first col
    output_arr[2] = distance_hand_knee
    output_arr[3] = is_action

    output_csv = np.vstack((output_csv, output_arr))

np.savetxt(output_file_path, output_csv, delimiter = ',',fmt="%s")

