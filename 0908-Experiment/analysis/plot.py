# 特徴量をプロットするファイル
# 実行例: python3 result_plot.py feature_csv_files/20230908111....csv

import sys
import os
import matplotlib.pyplot as plt

input_csv = sys.argv[1] # feature_csv_files/20230908....
select_colmn = int(sys.argv[2]) # プロットしたい特徴量, 0, 1, 2 を選択
list_feature = ['doc_hand_knee', 'doc_elbow_angle', 'doc_wrist_angle', 'pat_wrist_angle', 'pair_shoulder', 'pair_hip']
dir_path = f"plot_files/{list_feature[select_colmn]}"
base_name = os.path.splitext(os.path.basename(input_csv))[0]
output_file_path = f"{dir_path}/{base_name}-{list_feature[select_colmn]}.png"

with open(input_csv) as csv:
    time_array = []
    action_status = []
    feature_array = []
    for row in csv:
        # row 0:video_time, 1:action_now, 2:hand_knee, 3:elbow_angle, 4:
        input_row = row.split(",")
        time_array.append(float(input_row[0]))
        action_status.append(float(input_row[1])*45)
        feature_array.append(float(input_row[select_colmn+2]))

plt.figure()
plt.plot(time_array, feature_array)
# plt.plot(time_array, action_status)
plt.title(list_feature[select_colmn] + '-' + base_name)
plt.savefig(output_file_path, format="png", dpi=300)