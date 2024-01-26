#!/bin/sh
if [ ! -d data_csv_files ]; then
  mkdir data_csv_files
fi

if [ ! -d feature_csv_files ]; then
  mkdir feature_csv_files
fi

data_parent=$1 # もとデータが配置されているディレクトリを指定する．カレントディレクトリの場合何も指定せずに実行
a_dirs=`ls -d *20231103*`
b_dirs=`ls -d *20230908*`

echo 1103 $a_dirs
for dir in $a_dirs; do
  # analysis2.py doc_csv_path pat_csv_path output_csv_path fps
  echo "${dir} analysis"
  python3 feature_analysis.py $dir ./data_csv_files ./feature_csv_files 10

done

echo 0908 $b_dirs
for dir in $b_dirs; do
  # analysis2.py doc_csv_path pat_csv_path output_csv_path fps
  echo "${dir} analysis"
  python3 feature_analysis.py $dir ./data_csv_files ./feature_csv_files 20
  python3 downsample.py "feature_csv_files/${dir}.csv" "feature_csv_files/0908down/${dir}-down.csv"
done

echo cp to R-projects "~/Desktop/R-docker/R/phyisical"
cp -r feature_csv_files ~/Desktop/R-docker/R/phyisical