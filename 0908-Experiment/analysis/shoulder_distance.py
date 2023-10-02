import sys
import math
from matplotlib import pyplot
import numpy as np

input_csv = sys.argv[1] #csv ファイルセレクト
# output_csv_path = sys.argv[2]

with open(input_csv) as file:
  for line in file:
    input_arr = line.split(",")