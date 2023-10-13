# 特徴量をプロットするファイル
# 実行例: python3 result_plot.py feature_csv_files/20230908111....csv

import sys
import os
import math
import matplotlib.pyplot as plt
import numpy as np

list_feature = ['HandToKnee', 'ElbowAngle']
input_csv = sys.argv[1]
base_name = os.path.splitext(os.path.basename(input_csv))[0]
hand_knee_path = 'plot_files/hand_knee/' + base_name + '-' + list_feature[0] + '.png'
elbow_path = 'plot_files/elbow_angle/' + base_name + '-' + list_feature[1] + '.png'

with open(input_csv) as csv:
    time_array = []
    y_array = []
    y1_array = []
    y2_array = []
    for row in csv:
        input_row = row.split(",")
        time_array.append(float(input_row[0]))
        y_array.append(float(input_row[1])*45)
        y1_array.append(float(input_row[2]))
        y2_array.append(float(input_row[3]))

plt.figure()
plt.plot(time_array, y1_array)
plt.plot(time_array, y_array)
plt.title(list_feature[0] + '-' + base_name)
plt.savefig(hand_knee_path, format="png", dpi=300)

plt.figure()
plt.plot(time_array, y2_array)
plt.plot(time_array, y_array)
plt.title(list_feature[1] + '-' + base_name)
plt.savefig(elbow_path, format="png", dpi=300)