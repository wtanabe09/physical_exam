# 特徴量をプロットするファイル
# 実行例: python3 result_plot.py feature_csv_files/20230908111....csv
# list_feature = ['doc_hand_knee', 'doc_elbow_angle', 'doc_wrist_angle', 'doc_shoulder_hip', 'pat_wrist_angle', 'pat_elbow_angle', 'pair_shoulder', 'pair_hip', 'pair_face']

import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

# input_csv = sys.argv[1] # feature_csv_files/20230908....
myaku_csv = [
    "feature_csv_files/0908down/20230908111605978565-down.csv", 
    "feature_csv_files/0908down/20230908111906452490-down.csv", 
    "feature_csv_files/0908down/20230908112332510780-down.csv"    
]

colors = ["blue","green","red","black"]      # 各プロットの色
labels = ["a","b","c","d"]

# data = pd.read_csv(myaku_csv[0], encoding="UTF8")
# data_x = data[data.columns[0]]

for i, data in enumerate(myaku_csv):
    print(i)
    data = pd.read_csv(myaku_csv[i], encoding="UTF8")
    data_x = data[data.columns[0]]
    data_y = data[data.columns[2]]
    ax.plot(data_x, data_y, color=colors[i], label=labels[i])

# plt.plot(time_array, action_status)
# plt.title(output_path)
plt.show()
# plt.savefig(output_path, format="png", dpi=300)