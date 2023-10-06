import sys
import math
import matplotlib.pyplot as plt
import numpy as np

input_csv = sys.argv[1]

with open(input_csv) as csv:
    time_array = []
    distance_array = []
    elbow_angle = []
    for row in csv:
        input_row = row.split(",")
        time_array.append(float(input_row[1]))
        distance_array.append(float(input_row[2]))
        elbow_angle.append(float(input_row[3]))


# plt.plot(time_array, distance_array)
# plt.title('Distance from wrist to knee')
# plt.savefig("results/distance_wrist_knee.png", format="png", dpi=300)
# plt.show()

plt.plot(time_array, elbow_angle)
plt.title('Angle of Elbow')
plt.savefig("results/elbow_angle.png", format="png", dpi=300)
