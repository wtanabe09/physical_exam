#!/bin/sh
if [ ! -d analysis_csv_files ]; then
  mkdir feature_csv_files
fi

if [ ! -d plot_files ]; then
  mkdir plot_files
fi

data_parent=$@  # data_csv_files/*-doc.csv の相対パスをコマンドライン引数で指定
data_files=`ls $data_parent`

for file in $data_files; do
  python3 analysis.py "data_csv_files/${file##*/}" "feature_csv_files/${file##*/}"
  python3 plot.py "feature_csv_files/${file##*/}" "0" # 特徴量1をプロット
  python3 plot.py "feature_csv_files/${file##*/}" "1" # 特徴量2をプロット
  echo "created ${file##*/}"
done

echo 'done'