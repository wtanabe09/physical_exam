#!/bin/sh

if [ ! -d data_csv_files ]; then
  mkdir data_csv_files
fi

parent=$@  # Result_chair or Result_bed の相対パスをコマンドライン引数で指定
dirs=`ls $parent`

for dir in $dirs; do
  python3 txt_to_csv.py "${parent}/${dir}/${dir}_1.txt" "data_csv_files/${dir}-doc.csv"
  python3 txt_to_csv.py "${parent}/${dir}/${dir}_2.txt" "data_csv_files/${dir}-doc.csv"
done

echo 'done'