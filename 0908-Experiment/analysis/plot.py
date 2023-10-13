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
result_png_path1 = 'plot_files/' + base_name + '-' + list_feature[0] + '.png'
result_png_path2 = 'plot_files/' + base_name + '-' + list_feature[1] + '.png'

with open(input_csv) as csv:
    time_array = []
    y_array = []
    y2_array = []
    for row in csv:
        input_row = row.split(",")
        time_array.append(float(input_row[0]))
        y_array.append(float(input_row[1]))
        y2_array.append(float(input_row[2]))

plt.figure()
plt.plot(time_array, y_array)
plt.title(list_feature[0] + '-' + base_name)
plt.savefig(result_png_path1, format="png", dpi=300)

# plt.figure()
# plt.plot(time_array, y2_array)
# plt.title(list_feature[1] + '-' + base_name)
# plt.savefig(result_png_path2, format="png", dpi=300)