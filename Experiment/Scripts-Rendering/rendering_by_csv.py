# 特徴量描画動画・画像を保存するためのフィアル
# 実行時引数: python3 rendering_by_csv.py timestamp input_video_dir input_datacsv_dir input_featurecsv_dir output_video_image_dir
# 実行時引数例: python3 rendering_by_csv.py 20230908111226366962 ../Fixdata-Analysis/videos ../Fixdata-Analysis/data_csv_files ../Fixdata-Analysis/feature_csv_files ../Fixdata-Analysis/rendering_images_videos

# 必要なパッケージのインポート
import sys
import cv2
import pandas as pd
import math

lines = ((0,1),(0,4),(6,8),(3,7),(10,9), #顔
         (11,12),(12,24),(11,23),(23,24), #胴体
         (11,13),(13,15),(15,21),(15,17),(15,19),(17,19), #左腕
         (12,14),(14,16),(16,22),(16,18),(16,20),(18,20), #右腕
         (23,25),(25,27),(27,29),(27,31), #左脚
         (24,26),(26,28),(28,30),(28,32) #右脚
        )

# def draw_coordinate_by_holistics(img, pose_landmark, lines): #pose_landmark{{p1.x, p2y}, ...}
#     h, w = img.shape[:2]
#     for i in range(len(pose_landmark)):
#         pxy = int(pose_landmark[i].x * w), int(pose_landmark[i].y * h)
#         cv2.circle(img, pxy, 4, (0,255,0), 2, cv2.FILLED)
    
#     for line in lines:
#         p1xy = int(pose_landmark[line[0]].x * w), int(pose_landmark[line[0]].y * h)
#         p2xy = int(pose_landmark[line[1]].x * w), int(pose_landmark[line[1]].y * h)
#         cv2.line(img, p1xy, p2xy, (0,255,0), 2)

def draw_coordinate_by_csvarray(img, csv_array, lines):
    for i in range(0,33):
        try:
            pxy = int(csv_array[i*2+0]), int(csv_array[i*2+1])
            if(i <= 8):
                radius, thickness = 8, 5
            else:
                radius, thickness = 3, 2
            cv2.circle(img, pxy, radius, (0,255,0), thickness, cv2.FILLED)
        except:
           continue
    for line in lines:
        try:
            p1xy = int(csv_array[line[0]*2+0]), int(csv_array[line[0]*2+1])
            p2xy = int(csv_array[line[1]*2+0]), int(csv_array[line[1]*2+1])
            cv2.line(img, p1xy, p2xy, (0,255,0), 2)
        except:
            continue

def draw_feature_values(img, feature_array):
    h, w = img.shape[:2]
    for idx, feature_data in enumerate(feature_array):
        try:
            feature_values = math.floor(float(feature_data) * 1000) / 1000
        except:
            feature_values = 0
        text = f"{feature_csv_headers[idx]}: " + str(feature_values)
        cv2.putText(img, text, (w-280, (idx+1)*25), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0,126,255), 2)

# 実行時引数：python3 rendering.py timestamp[1] video_parent_dir[2] data_dir[3] feature_dir[4] rendering_dir[5]
timestamp = sys.argv[1]
input_video_path = sys.argv[2] + "/" + timestamp + ".mp4"
# input_video_path = sys.argv[2] + "/" + timestamp + "_1.mp4" # for *2023* data
doctor_csv_path = sys.argv[3] + "/" + timestamp + "-1.csv"
patient_csv_path = sys.argv[3] + "/" + timestamp + "-2.csv"
feature_csv_path = sys.argv[4] + "/" + timestamp + ".csv"
output_video_path = sys.argv[5] + "/videos/" + timestamp + ".mp4"
# output_image_path = sys.argv[5] + "/images/" + timestamp + ".png"

# file path for testing
# doctor_csv_path = './Fixdata-Analysis/data_csv_files/20230908111226366962-1.csv'
# patient_csv_path = './Fixdata-Analysis/data_csv_files/20230908111226366962-2.csv'
# feature_csv_path = './Fixdata-Analysis/feature_csv_files/20230908111226366962.csv'
# output_video_path = './Fixdata-Analysis/rendering/outtest-no-feature.mp4'
# output_image_path = './Fixdata-Analysis/rendering/outtest-no-feature.png'

# read csv
doctor_csv = pd.read_csv(doctor_csv_path).values.tolist()
patient_csv = pd.read_csv(patient_csv_path).values.tolist()
feature_csv = pd.read_csv(feature_csv_path, header=None).values.tolist()
feature_csv_headers = feature_csv[0]
feature_csv_values = feature_csv[1:]

# input movie, create movie writer
cap = cv2.VideoCapture(input_video_path)
frame_rate = cap.get(cv2.CAP_PROP_FPS)
frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
size = (width, height) # 動画の画面サイズ
fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v') # ファイル形式(ここではmp4)
writer = cv2.VideoWriter(output_video_path, fmt, frame_rate, size) # ライター作成
print(f"fps: {frame_rate}, frame_count: {frame_count}")

count = 0

while cap.isOpened():
    success, image = cap.read()

    if not success:
        print("Ignoring empty camera frame.")
        break

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # set array to csv data
    image.flags.writeable = False
    doc_array = doctor_csv[count][1:]
    pat_array = patient_csv[count][1:]
    fea_array = feature_csv_values[count]

    # draw landmark
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    draw_coordinate_by_csvarray(image, doc_array, lines) # 医者の骨格座標表示
    draw_coordinate_by_csvarray(image, pat_array, lines) # 患者の骨格座標表示
    draw_feature_values(image, fea_array) # 姿勢特徴量の数値描画

    # if count == 200:
    #     cv2.imwrite(output_image_path, image)
    #     print("save image")

    writer.write(image) # 画像を1フレーム分として書き込み

    # テスト用：描画状況を確認できる
    # cv2.imshow('MediaPipe Holistic', image)
    # if cv2.waitKey(5) & 0xFF == 27:
    #   break

    count+=1

cap.release()
writer.release()
print("finish!")