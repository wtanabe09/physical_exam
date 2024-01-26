import csv
import pandas as pd
from scipy.stats import ttest_ind
import itertools

# 1103 fps 10, 0908 fps 20
myaku = (
    ('0_c_20231103101658683273', '25.5', '10', 'c'), #0
    ('20230908111605978565', '9.4', '20', 'b'), #1
    ('20230908111906452490', '16', '20', 'c'), #2
    ('20230908112332510780', '10', '20', 'd') #3
)

files = myaku

output_txt = '../Fixdata-Analysis/ttest_result.txt'

# データ読み込みと前処理 csv読み込んで配列化する Dataframeを作成する
datas = []
headers = []
for file_idx, file in enumerate(files):
    input_file = f'../Fixdata-Analysis/feature_csv_files/{file[0]}.csv'
    target_line = float(file[1]) * int(file[2]) + 1 # 秒数*fps 行目を見る
    with open(input_file) as csvfile:
        csv_reader = csv.reader(csvfile)
        if file_idx == 0:
            headers = next(csv_reader)
        for i, line in enumerate(csv_reader):
            if i == target_line:
                datas.append(line)

df = pd.DataFrame(datas, dtype=float)
df.columns = headers
df.index = [r[0] for r in files]

# 書き込みファイル初期化
with open(output_txt, 'w') as file:
    file.write('')
# 全ての特徴量の全ての組み合わせについてT検定を行う
for col_name, item in df.items():
    print(col_name)
    # t検定のための組み合わせを生成して実行
    t_results = []
    # 2:2, 1:3の組み合わせ作成
    for n in [1, 2]:
        for comb in itertools.combinations(df.index, n):
            if comb == (1, 2) or comb == (1, 3) or comb == (2, 3): continue
            a = df.loc[list(comb)][col_name]
            b = df.drop(list(comb))[col_name]
            result = ttest_ind(list(a), list(b))
            t_results.append((result[1], (list(a.index), list(b.index))))
            print(f"T-test for group {list(a.index)},{list(b.index)}:{result[1]}")

            if result[1] <= 0.06:
                with open(output_txt, 'a') as file:
                    file.write(f"T-test for group {list(a.index)},{list(b.index)}:{result[1]}\n")