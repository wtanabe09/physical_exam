#!/bin/sh

if [ ! -d csv_files ]; then
  mkdir csv_files
fi

parent=$@  # Result_face_to_face or Result_bed の相対パス
dirs=`ls $parent`

for dir in $dirs; do
  python3 txt_to_csv.py "${parent}/${dir}/${dir}_1.txt" "csv_files/${dir}_1.csv"
  python3 txt_to_csv.py "${parent}/${dir}/${dir}_2.txt" "csv_files/${dir}_2.csv"
done

echo 'done'