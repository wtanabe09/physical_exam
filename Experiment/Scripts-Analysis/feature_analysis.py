# 特徴量のCSVファイルをつくるプログラム
# 医者骨格座標CSV，患者骨格座標CSVを入力し，姿勢特徴量CSVを出力

import sys
import numpy as np
import math
from calc_feature import distance, inner_product, x_distance, max_a_to_b

# 医者のみの特徴量の計算
def calc_doctor_feature(doc_arr, doctor_csv):
    # 座標の抽出 index:ラベル番号*2(各ポイントx,yあるから)+1(タイムスタンプカラム)
    nose = np.array([float(doc_arr[1]), float(doc_arr[2])])
    right_index = np.array([float(doc_arr[(19*2)+1]), float(doc_arr[(19*2)+2])])
    right_knee = np.array([float(doc_arr[(25*2)+1]), float(doc_arr[(25*2)+2])])
    right_shoulder = np.array([float(doc_arr[(11*2)+1]), float(doc_arr[(11*2)+2])]) # 右肩（左肩インデックス）
    right_elbow = np.array([float(doc_arr[(13*2)+1]), float(doc_arr[(13*2)+2])]) # 右肘
    right_wrist = np.array([float(doc_arr[(15*2)+1]), float(doc_arr[(15*2)+2])]) # 右手首
    right_hip = np.array([float(doc_arr[(23*2)+1]), float(doc_arr[(23*2)+2])]) # 右腰（左肩インデックス）
    max_shoulder_hip = max_a_to_b(doctor_csv, 11, 23) # max of hip to knee

    # 特徴量計算 上で得た座標を用いて
    # shoulder_hip = distance(right_shoulder, right_hip)
    dist_hand_knee = x_distance(right_knee, right_wrist) / max_shoulder_hip # 計算：右手と右膝のx座標の距離，-は手が膝よりも後ろにある
    dist_hand_nose = x_distance(right_wrist, nose) / max_shoulder_hip
    angle_elbow = inner_product(right_shoulder, right_elbow, right_wrist) # 計算：肘角度
    angle_wrist = inner_product(right_elbow, right_wrist, right_index) # 計算：手首の角度
    angle_hip = inner_product(right_shoulder, right_hip, right_knee)

    return dist_hand_knee, dist_hand_nose, angle_elbow, angle_wrist, angle_hip

# 患者のみの特徴量の計算
def calc_patient_feature(pat_arr):
    left_index = np.array([float(pat_arr[(20*2)+1]), float(pat_arr[(20*2)+2])])
    left_shoulder = np.array([float(pat_arr[(12*2)+1]), float(pat_arr[(12*2)+2])]) # 左肩（左肩インデックス）
    left_elbow = np.array([float(pat_arr[(14*2)+1]), float(pat_arr[(14*2)+2])]) # 右肘
    left_wrist = np.array([float(pat_arr[(16*2)+1]), float(pat_arr[(16*2)+2])]) # 右手首

    elbow_angle = inner_product(left_shoulder, left_elbow, left_wrist) # 計算：手首の角度
    wrist_angle = inner_product(left_elbow, left_wrist, left_index) # 計算：手首の角度

    return elbow_angle, wrist_angle

# 医者と患者の特徴量の計算
def calc_pair_feature(doc_arr, pat_arr, doctor_csv):
    doc_nose = np.array([float(doc_arr[(0*2)+1]), float(doc_arr[(0*2)+2])]) # 鼻
    doc_right_shoulder = np.array([float(doc_arr[(11*2)+1]), float(doc_arr[(11*2)+2])]) # 右肩（左肩インデックス）
    doc_right_hip = np.array([float(doc_arr[(23*2)+1]), float(doc_arr[(23*2)+2])]) # 右腰（左肩インデックス）
    doc_max_shoulder_hip = max_a_to_b(doctor_csv, 11, 23)

    pat_nose = np.array([float(pat_arr[(0*2)+1]), float(pat_arr[(0*2)+2])]) # 鼻
    pat_left_shoulder = np.array([float(pat_arr[(12*2)+1]), float(pat_arr[(12*2)+2])]) # 右肩（左肩インデックス）
    pat_left_hip = np.array([float(pat_arr[(24*2)+1]), float(pat_arr[(24*2)+2])]) # 右腰（左肩インデックス）
    
    
    face_x_distance = x_distance(doc_nose, pat_nose) / doc_max_shoulder_hip
    shoulder_distance = x_distance(doc_right_shoulder, pat_left_shoulder) / doc_max_shoulder_hip
    hip_distace = x_distance(doc_right_hip, pat_left_hip) / doc_max_shoulder_hip

    return shoulder_distance, hip_distace, face_x_distance


def main():
    if len(sys.argv) != 5:
        print("Usage: python3 analysis.py timestamp doctor_csv_dir result_csv_path fps")
        return

    timestamp = sys.argv[1] # *2023*
    doctor_csv = sys.argv[2] + "/" + timestamp + "-1.csv" # ./data_csv_files/
    patient_csv = sys.argv[2] + "/" + timestamp + "-2.csv" # ./data_csv_files/**-2.csv
    result_csv_path = sys.argv[3] + "/" + timestamp + ".csv" # ./feature_csv_files/***.csv
    fps = int(sys.argv[4]) # 10 or 20 or 30
    
    row_counter = 0
    result_csv = []
    header = np.array([
        "time", 
        "doc_dist_x_hand_knee", "doc_dist_x_hand_nose", "doc_angle_elbow", "doc_angle_wrist", "doc_angle_hip",
        "pat_angle_elbow", "pat_angle_wrist",
        "pair_dist_shoulder", "pair_dist_hip", "pair_dist_face"
        ])

    with open(doctor_csv) as doctor, open(patient_csv) as patient:
        next(doctor)
        next(patient)
        for doctor_line, patient_line in zip(doctor, patient):
            doc_line = doctor_line.split(",")
            pat_line = patient_line.split(",")

            doc_dist_hand_knee, doc_dist_hand_nose, doc_angle_elbow, doc_angle_wrist, doc_angle_hip = calc_doctor_feature(doc_line, doctor_csv)
            pat_elbow_angle, pat_wrist_angle = calc_patient_feature(pat_line)
            pair_shoulder_distance, pair_hip_distance, pair_face_distance = calc_pair_feature(doc_line, pat_line, doctor_csv)

            result_arr = np.array([
                math.floor(row_counter/fps * 100) / 100, #0

                doc_dist_hand_knee, #1
                doc_dist_hand_nose,
                doc_angle_elbow,
                doc_angle_wrist,
                doc_angle_hip,

                pat_elbow_angle, #5
                pat_wrist_angle,

                pair_shoulder_distance, #7
                pair_hip_distance,
                pair_face_distance
            ], dtype=float)
            result_csv.append(result_arr)

            row_counter += 1

    result_csv = np.vstack((header, result_csv))
    np.savetxt(result_csv_path, result_csv, delimiter=',', fmt="%s")

if __name__ == "__main__":
    main()
