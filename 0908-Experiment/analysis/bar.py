import time
import datetime
import sys
# import calc_feature

feature_file = sys.argv[1] # feature_csv_files
with open(feature_file) as f:
    line = f.read().splitlines()
    num_of_line = len(line)

    for i in range(0, num_of_line, 20):
        line_arr = line[i].split(",")
        dt_now = datetime.datetime.now()
        micro_val = dt_now.microsecond / 1000000
        print(round(float(line_arr[6])), end=" ")
        for j in range(round(float(line_arr[6])/10)):
            print('*', end='')
        print()
        time.sleep(1 - micro_val)
    
# print(line, num_line)