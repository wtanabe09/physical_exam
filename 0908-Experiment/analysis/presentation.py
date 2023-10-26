import time
import datetime
import sys
# import calc_feature

feature_file = sys.argv[1] # feature_csv_files
second = 0
# hip_distance = 6

with open(feature_file) as f:
    lines = f.read().splitlines()
    num_of_line = len(lines)
    video_second = round(float(lines[num_of_line-1].split(",")[0]))

    for i in range(19, num_of_line, 20):
        line_arr = lines[i].split(",")
        dt_now = datetime.datetime.now()
        micro_val = dt_now.microsecond / 1000000

        doc_hand_knee = round(float(line_arr[2])*10)
        face_distance = round(float(line_arr[10]))
        pat_elbow_angle = round(float(line_arr[3]))

        print(f"{line_arr[second]}/{video_second}")

        print("医者-患者,顔の距離: ", face_distance, end=" ")
        for j in range(face_distance * 5):
            print('▪︎', end='')
        print()

        print("医者,手と膝の距離 : ", doc_hand_knee, end=" ")
        for j in range(doc_hand_knee * 5):
            print('▪︎', end='')
        print()

        print("医者,肘の角度     : ", pat_elbow_angle, end=" ")
        for j in range(round(pat_elbow_angle / 5)):
            print('▪︎', end='')
        print()
    
        time.sleep(1 - micro_val)