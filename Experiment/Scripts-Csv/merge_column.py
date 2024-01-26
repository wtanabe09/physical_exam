# 1/17 ディレクトリ内の全てのCSVファイルにおいて指定行を結合する
# 例えばcsvfilesディレクトリにある全てCSVファイルの１行目を結合したCSVファイルを作成する

import pandas as pd
import os

# 結合するCSVファイルが格納されているディレクトリを指定
directory_path = '/path/to/csv/files'

# CSVファイルの一覧を取得
csv_files = [file for file in os.listdir(directory_path) if file.endswith('.csv')]

# 最終的な結果を格納するデータフレームを作成
result_df = pd.DataFrame()

# 各CSVファイルから1列目を取り出し、結合
for csv_file in csv_files:
    file_path = os.path.join(directory_path, csv_file)
    df = pd.read_csv(file_path, usecols=[0])  # 1列目だけを取り出す
    result_df = pd.concat([result_df, df], axis=1) # axis=1 横方向に結合

# 列の名前を設定（任意）
result_df.columns = [f'File_{i+1}' for i in range(len(csv_files))]

# 結果を出力
print(result_df)