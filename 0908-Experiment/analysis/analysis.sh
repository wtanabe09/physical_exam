#!/bin/sh
if [ ! -d analysis_csv_files ]; then
  mkdir feature_csv_files
fi

if [ ! -d plot_files ]; then
  mkdir plot_files
fi

data_parent=$@  # data_csv_files の相対パスをコマンドライン引数で指定
data_dirs=`ls $data_parent`

for dir in $data_dirs; do
  python3 analysis2.py "data_csv_files/${dir}/${dir}-doc.csv" "data_csv_files/${dir}/${dir}-pat.csv" "feature_csv_files/${dir}.csv"
  # python3 plot.py "feature_csv_files/${dir}.csv" "5" # 特徴量1をプロット
  # python3 plot.py "feature_csv_files/${file}-doc.csv" "1" # 特徴量2をプロット
  # echo "create ${dir}"
done

echo 'done'