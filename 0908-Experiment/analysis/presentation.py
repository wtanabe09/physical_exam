import time
import datetime
import sys
# import calc_feature

feature_file = sys.argv[1] # feature_csv_files
second = 0
hand_knee = 2
elbow_angle = 3
hip_distance = 6
face_distance = 9

with open(feature_file) as f:
    line = f.read().splitlines()
    num_of_line = len(line)

    for i in range(19, num_of_line, 20):
        line_arr = line[i].split(",")
        dt_now = datetime.datetime.now()
        micro_val = dt_now.microsecond / 1000000

        print(line_arr[second])

        print("医者-患者,顔の距離: ", round(float(line_arr[face_distance])), end=" ")
        for j in range(round(float(line_arr[face_distance])/10)):
            print('*', end='')
        print()

        print("医者,手と膝の距離 :  ", round(float(line_arr[hand_knee])), end=" ")
        for j in range(round(float(line_arr[hand_knee])/5)):
            print('*', end='')
        print()

        print("医者,肘の角度     :  ", round(float(line_arr[elbow_angle])), end=" ")
        for j in range(round(float(line_arr[elbow_angle])/5)):
            print('*', end='')
        print()
    
        time.sleep(1 - micro_val)