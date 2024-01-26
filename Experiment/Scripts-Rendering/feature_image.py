import cv2
import sys
import csv


def save_frame(video_path, result_path, frame_sec):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    # print(f"fps: {fps}")
    frame_num = frame_sec * fps

    if not cap.isOpened():
        return

    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
    ret, frame = cap.read()

    if ret:
        cv2.imwrite(result_path, frame)


input_feature_video_dir = sys.argv[1]
output_feature_image_dir = sys.argv[2]
time_csv = sys.argv[3]
# csvファイルからファイルと，切り抜き秒数を取得
# time_data: timestamp, frame_sec, person, kind_of_technique
with open(time_csv) as time_file:
    for line in time_file:
        time_data = line.rstrip('\n').split(",")
        print(time_data)
        input_feature_video_path = input_feature_video_dir + "/" + time_data[0] + ".mp4"
        output_feature_image_path = f"{output_feature_image_dir}/{time_data[3]}-{time_data[2]}-{time_data[0]}.png"
        frame_sec = float(time_data[1])
        save_frame(input_feature_video_path, output_feature_image_path, frame_sec)



