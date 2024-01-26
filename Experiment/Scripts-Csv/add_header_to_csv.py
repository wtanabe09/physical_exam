# csvファイルにヘッダーを追加し，指定の保存先に保存する
# python3 input_csv output_csv

import pandas as pd
import sys
import math

# CSVファイルの読み込み
in_csv_path = sys.argv[1]
out_csv_path = sys.argv[1]
fps = int(sys.argv[2])

# for test
# in_csv_path = "../kut-sample-video/data_csv_files/01_脈1-C-2.csv"
# out_csv_path = "../kut-sample-video/data_csv_files/01_脈1-C-2.csv"
# fps = 30

df = pd.read_csv(in_csv_path, header=None)

# headerのラベルデータを作成
id_labels = []
for i in range(33):
    id_labels.append(f"{i}.x")
    id_labels.append(f"{i}.y")

# ラベルを1行目に追加
df.columns = id_labels + list(df.columns[len(id_labels):])

# タイムスタンプのカラムのデータを作成
timestamp_data = []
length = len(df)
for l in range(0, len(df)):
    data = math.floor(l/fps*100)/100
    timestamp_data.append(data)
# print(timestamp_data)
# 新しいカラムを1列目に追加
df.insert(0, 'timestamp', timestamp_data)

# 変更を保存
df.to_csv(out_csv_path, index=False)