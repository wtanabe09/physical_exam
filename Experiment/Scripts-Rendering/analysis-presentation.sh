#!/bin/sh
if [ ! -d data_csv_files ]; then
  mkdir data_csv_files
fi

if [ ! -d feature_csv_files ]; then
  mkdir feature_csv_files
fi

if [ ! -d feature_videos ]; then
  mkdir feature_videos
fi

# data_parent=$@  # 20230908 への相対パスをコマンドライン引数で指定
# data_dirs=`ls $data_parent`

data=$@
dirs=`ls $data`
dir=`basename $data`
# for dir in $dirs; do

  # txt_to_csv.py input_path output_path
  python3 txt_to_csv.py "${dir}/${dir}_1.txt" "data_csv_files/${dir}-doc.csv"
  python3 txt_to_csv.py "${dir}/${dir}_2.txt" "data_csv_files/${dir}-pat.csv"
  # analysis2.py doc_csv_path pat_csv_path output_csv_path
  python3 analysis2.py "data_csv_files/${dir}-doc.csv" "data_csv_files/${dir}-pat.csv" "feature_csv_files/${dir}.csv"
  # presentation.py feature_csv input_video output_video
  python3 presentation.py "feature_csv_files/${dir}.csv" "${dir}/${dir}_result.mp4" "feature_videos/${dir}_feature.mp4"
# done