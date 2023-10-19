import sys
import os
import numpy as np
from calc_feature import distance, inner_product

def calc_doctor_feature(doc_arr):
    right_index = np.array([float(doc_arr[(19*2)+1]), float(doc_arr[(19*2)+2])])
    right_knee = np.array([float(doc_arr[(25*2)+1]), float(doc_arr[(25*2)+2])])
    right_shoulder = np.array([float(doc_arr[(11*2)+1]), float(doc_arr[(11*2)+2])]) # 右肩（左肩インデックス）
    right_elbow = np.array([float(doc_arr[(13*2)+1]), float(doc_arr[(13*2)+2])]) # 右肘
    right_wrist = np.array([float(doc_arr[(15*2)+1]), float(doc_arr[(15*2)+2])]) # 右手首

    hand_knee_distance = distance(right_index, right_knee) # 計算：右手から右膝までの距離
    elbow_angle = inner_product(right_shoulder, right_elbow, right_wrist) # 計算：肘角度
    wrist_angle = inner_product(right_elbow, right_wrist, right_index) # 計算：手首の角度

    return hand_knee_distance, elbow_angle, wrist_angle

def calc_patient_feature(pat_arr):
    right_index = np.array([float(pat_arr[(19*2)+1]), float(pat_arr[(19*2)+2])])
    right_shoulder = np.array([float(pat_arr[(11*2)+1]), float(pat_arr[(11*2)+2])]) # 右肩（左肩インデックス）
    right_elbow = np.array([float(pat_arr[(13*2)+1]), float(pat_arr[(13*2)+2])]) # 右肘
    right_wrist = np.array([float(pat_arr[(15*2)+1]), float(pat_arr[(15*2)+2])]) # 右手首

    wrist_angle = inner_product(right_elbow, right_wrist, right_index) # 計算：手首の角度

    return wrist_angle

def calc_pair_feature(doc_arr, pat_arr):
    doc_right_shoulder = np.array([float(doc_arr[(11*2)+1]), float(doc_arr[(11*2)+2])]) # 右肩（左肩インデックス）
    pat_right_shoulder = np.array([float(pat_arr[(11*2)+1]), float(pat_arr[(11*2)+2])]) # 右肩（左肩インデックス）
    doc_right_hip = np.array([float(doc_arr[(23*2)+1]), float(doc_arr[(23*2)+2])]) # 右腰（左肩インデックス）
    pat_right_hip = np.array([float(pat_arr[(23*2)+1]), float(pat_arr[(23*2)+2])]) # 右腰（左肩インデックス）
    
    
    shoulder_distance = distance(doc_right_shoulder, pat_right_shoulder)
    hip_distace = distance(doc_right_hip, pat_right_hip)

    return shoulder_distance, hip_distace


def main():
    if len(sys.argv) != 4:
        print("Usage: python3 analysis.py doctor_csv patient_csv result_csv_path")
        return

    doctor_csv = sys.argv[1]
    patient_csv = sys.argv[2]
    result_csv_path = sys.argv[3]
    base_name = os.path.splitext(os.path.basename(doctor_csv))[0]

    threshold = 45
    short_distance_count = 0
    action_number = 0
    result_csv = []

    bool_action_now = False
    row_counter = 0

    with open(doctor_csv) as doctor, open(patient_csv) as patient:
        for doctor_line, patient_line in zip(doctor, patient):
            doc_line = doctor_line.split(",")
            pat_line = patient_line.split(",")

            doc_hand_knee_distance, doc_elbow_angle, doc_wrist_angle = calc_doctor_feature(doc_line)
            pat_wrist_angle = calc_patient_feature(pat_line)
            pair_shoulder_distance, pair_hip_distance = calc_pair_feature(doc_line, pat_line)

            if bool_action_now: # 動作中
                if doc_hand_knee_distance > threshold: # 閾値より大きいなら動作中，何もしない．
                    short_distance_count = 0
                else: # 閾値以下なら手を膝に置いている．以下で膝に置いている時間が３秒以上続いているか確認する．
                    short_distance_count += 1
                    if short_distance_count >= 60: # 閾値以下 3秒以上続いたら動作終了処理
                        bool_action_now = False
                        action_number += 1
            else: # Not 動作
                if doc_hand_knee_distance > threshold: # 手が膝から離れたら動作開始
                    bool_action_now = True
                    short_distance_count = 0
                    action_number += 1

            row_counter += 1

            result_arr = np.array([
                round(row_counter / 20, 2),
                bool_action_now,
                doc_hand_knee_distance,
                doc_elbow_angle,
                doc_wrist_angle,
                pat_wrist_angle,
                pair_shoulder_distance,
                pair_hip_distance
            ], dtype=float)

            result_csv.append(result_arr)

    np.savetxt(result_csv_path, result_csv, delimiter=',', fmt="%s")
    # print("done")

if __name__ == "__main__":
    main()
