import numpy as np
import sys

input_file_path = sys.argv[1]
output_file_path = sys.argv[2]

output_csv = np.empty((0,67))
with open(input_file_path) as file:
    for line in file:
        input_arr = line.split(",")
        output_arr = np.zeros(66)
        for i in range(33):
            if str(i) in input_arr:
                point_index = input_arr.index(str(i))
                output_arr[i*2] = input_arr[point_index + 1]
                output_arr[i*2+1] = input_arr[point_index + 2]
            else:
                output_arr[i*2] = np.nan
                output_arr[i*2+1] = np.nan
        
        output_arr = np.hstack((input_arr[0], output_arr)) # add timestanp to first col
        output_csv = np.vstack((output_csv, output_arr))
    
np.savetxt(output_file_path, output_csv, delimiter = ',',fmt="%s")