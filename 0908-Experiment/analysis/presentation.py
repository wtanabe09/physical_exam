import sys
import os
import numpy as np
import math
import cv2

# 特徴量の描画を行うプログラム

def draw_feature(frame, pointA, pointB, pointC):
    a_width = int(pointA * 10)
    b_width = int(pointB * 12)
    c_width = int(pointC / 10)

    # (horizontal, vertical)
    cv2.putText(frame, 'distance', (40, 20), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), thickness=1)
    cv2.putText(frame, '{:.2f}'.format(pointA), (40, 45), cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 0, 255), thickness=1)
    for i in range(a_width):
        cv2.rectangle(frame, (130+(i*25), 30), (150+(i*25), 45), (0, 0, 255), thickness=-1)

    cv2.putText(frame, 'doctor hand to knee', (40, 65), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 0), thickness=1)
    cv2.putText(frame, '{:.2f}'.format(pointB), (40, 90), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 0, 0), thickness=1)
    for i in range(b_width):
        cv2.rectangle(frame, (130+(i*25), 75), (150+(i*25), 90), (255, 0, 0), thickness=-1)

    cv2.putText(frame, 'doctor elbow angle', (40, 110), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0), thickness=1)
    cv2.putText(frame, '{:.1f}'.format(pointC), (40, 135), cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 255, 0), thickness=1)
    for i in range(c_width):
        cv2.rectangle(frame, (130+(i*25), 120), (150+(i*25), 135), (0, 255, 0), thickness=-1)
    

if __name__ == "__main__":
    # python3 presentation.py 20230908111226366962.csv
    feature_csv = sys.argv[1]
    input_video = sys.argv[2]
    output_video = sys.argv[3]

    with open(feature_csv) as f_csv:
        csv_lines = f_csv.readlines()

    cap = cv2.VideoCapture(input_video)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    size = (width, height)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_rate = 20
    fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    writer = cv2.VideoWriter(output_video, fmt, frame_rate, size)

    for i in range(frame_count):
        ret, frame = cap.read()
        if ret == True:
            if i % 20 == 0:
                line_arr = csv_lines[i].split(",")
                face_distance = 0 if math.isnan(float(line_arr[10])) else float(line_arr[10])
                doc_hand_knee = 0 if math.isnan(float(line_arr[2])) else float(line_arr[2])
                doc_elbow_angle = 0 if math.isnan(float(line_arr[3])) else float(line_arr[3])
                pat_elbow_angle = 0 if math.isnan(float(line_arr[6])) else round(float(line_arr[6]))
                pat_wrist_angle = 0 if math.isnan(float(line_arr[7])) else round(float(line_arr[7]))
            draw_feature(frame, face_distance, doc_hand_knee, doc_elbow_angle)
            # cv2.imshow('frame', frame)
            writer.write(frame)
            # key = cv2.waitKey(30) & 0xFF
            # if key == ord('q'):
            #     break
        else:
            break

    writer.release()
    cap.release()
    cv2.destroyAllWindows()


