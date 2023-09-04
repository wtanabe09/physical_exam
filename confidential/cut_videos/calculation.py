# CSVデータからデータを取り出し分析を行うためのファイル

# import sys
# from turtle import distance
# import numpy as np
import math

def calc_distance(base_name):
    with open('./point_csv/'+base_name+'-C.csv') as f:

        distances = []
        for line in f:
            # 1行ごとの処理
            l = line.split(',')
            rigtht_hand_x = float(l[18*2])
            rigtht_hand_y = float(l[(18*2)+1])
            rigtht_knee_x = float(l[26*2])
            rigtht_knee_y = float(l[(26*2)+1])
            
            # 右手から右膝までの距離
            distance_hand_knee = math.sqrt((rigtht_hand_x - rigtht_knee_x)**2 + (rigtht_hand_y - rigtht_knee_y)**2)
            # print(distance_hand_knee)
            distances.append(distance_hand_knee)
    print('analysis.py, distances len :', len(distances))
    return distances
    