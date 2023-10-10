import sys
import os
import math
import matplotlib.pyplot as plt
import numpy as np

# 実行例: python3 result_plot.py 2 result_csv_files/20230908111...
y_colmn = int(sys.argv[1])
input_csv = sys.argv[2]
base_name = os.path.splitext(os.path.basename(input_csv))[0]
result_png_path = 'plot_png_files/' + base_name + '.png'
list_feature = ['HandToKnee', 'ElbowAngle']

with open(input_csv) as csv:
    time_array = []
    y_array = []
    for row in csv:
        input_row = row.split(",")
        time_array.append(float(input_row[1]))
        y_array.append(float(input_row[y_colmn]))

plt.plot(time_array, y_array)
plt.title(list_feature[y_colmn - 1] + '-' + base_name)
plt.savefig(result_png_path, format="png", dpi=300)
