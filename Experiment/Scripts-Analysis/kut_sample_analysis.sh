#!/bin/sh

files=`ls ../kut-sample-video *.mp4`
echo $files

for file in $files; do
    file_base=`basename $file .mp4`
    echo $file_base
    python3 feature_analysis.py $file_base ../kut-sample-video/data_csv_files ../kut-sample-video/feature_csv_files 30
done