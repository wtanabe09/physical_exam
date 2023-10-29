import sys
import math
import numpy as np
from calc_feature import distance, inner_product, x_distance, max_a_to_b

def calc_doctor_feature(doc_arr, doctor_csv):
    right_index = np.array([float(doc_arr[(19*2)+1]), float(doc_arr[(19*2)+2])])
    right_knee = np.array([float(doc_arr[(25*2)+1]), float(doc_arr[(25*2)+2])])
    right_shoulder = np.array([float(doc_arr[(11*2)+1]), float(doc_arr[(11*2)+2])]) # 右肩（左肩インデックス）
    right_elbow = np.array([float(doc_arr[(13*2)+1]), float(doc_arr[(13*2)+2])]) # 右肘
    right_wrist = np.array([float(doc_arr[(15*2)+1]), float(doc_arr[(15*2)+2])]) # 右手首
    right_hip = np.array([float(doc_arr[(23*2)+1]), float(doc_arr[(23*2)+2])]) # 右腰（左肩インデックス）
    max_shoulder_hip = max_a_to_b(doctor_csv, 11, 23) # max of hip to knee

    shoulder_hip = distance(right_shoulder, right_hip)
    hand_knee = distance(right_knee, right_index) # 計算：右手と右膝のx座標の距離，-は手が膝よりも後ろにある
    normal_hand_knee = hand_knee / max_shoulder_hip # 正規化
    elbow_angle = inner_product(right_shoulder, right_elbow, right_wrist) # 計算：肘角度
    wrist_angle = inner_product(right_elbow, right_wrist, right_index) # 計算：手首の角度

    return normal_hand_knee, elbow_angle, wrist_angle, shoulder_hip

def calc_patient_feature(pat_arr):
    left_index = np.array([float(pat_arr[(20*2)+1]), float(pat_arr[(20*2)+2])])
    left_shoulder = np.array([float(pat_arr[(12*2)+1]), float(pat_arr[(12*2)+2])]) # 左肩（左肩インデックス）
    left_elbow = np.array([float(pat_arr[(14*2)+1]), float(pat_arr[(14*2)+2])]) # 右肘
    left_wrist = np.array([float(pat_arr[(16*2)+1]), float(pat_arr[(16*2)+2])]) # 右手首

    elbow_angle = inner_product(left_shoulder, left_elbow, left_wrist) # 計算：手首の角度
    wrist_angle = inner_product(left_elbow, left_wrist, left_index) # 計算：手首の角度

    return elbow_angle, wrist_angle

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
    if len(sys.argv) != 4:
        print("Usage: python3 analysis.py doctor_csv patient_csv result_csv_path")
        return

    doctor_csv = sys.argv[1]
    patient_csv = sys.argv[2]
    result_csv_path = sys.argv[3]

    bool_action_now = False
    threshold = 45
    short_distance_count = 0
    action_number = 0
    row_counter = 0
    result_csv = []

    with open(doctor_csv) as doctor, open(patient_csv) as patient:
        for doctor_line, patient_line in zip(doctor, patient):
            doc_line = doctor_line.split(",")
            pat_line = patient_line.split(",")

            doc_hand_knee_distance, doc_elbow_angle, doc_wrist_angle, doc_shoulder_hip = calc_doctor_feature(doc_line, doctor_csv)
            pat_elbow_angle, pat_wrist_angle = calc_patient_feature(pat_line)
            pair_shoulder_distance, pair_hip_distance, pair_face_distance = calc_pair_feature(doc_line, pat_line, doctor_csv)

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
                round(row_counter/20, 2), #0
                bool_action_now, #1

                doc_hand_knee_distance, #2
                doc_elbow_angle,
                doc_wrist_angle,
                doc_shoulder_hip,

                pat_elbow_angle, #6
                pat_wrist_angle,

                pair_shoulder_distance, #8
                pair_hip_distance,
                pair_face_distance
            ], dtype=float)

            result_csv.append(result_arr)

    np.savetxt(result_csv_path, result_csv, delimiter=',', fmt="%s")

if __name__ == "__main__":
    main()
