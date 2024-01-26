# 0908:fps20, 1103:fps10 であるため，0908をダウンサンプリング
import sys
import csv

def downsample_data(input_file, output_file, original_fps, target_fps):
    downsample_factor = original_fps // target_fps

    with open(input_file, 'r') as input_csv, open(output_file, 'w', newline='') as output_csv:
        reader = csv.reader(input_csv)
        writer = csv.writer(output_csv)

        # ヘッダーをコピー
        header = next(reader)
        writer.writerow(header)

        # データを間引いて書き込む
        for row in reader:
            if reader.line_num % downsample_factor == 0:
                writer.writerow(row)

# 例として、fps 20のデータをfps 10に間引いて保存する
input_file_path = sys.argv[1] # 'feature_csv_files/20230908111226366962.csv'
output_file_path = sys.argv[2] # 'feature_csv_files/20230908111226366962.csv'
original_fps = 20
target_fps = 10

downsample_data(input_file_path, output_file_path, original_fps, target_fps)
