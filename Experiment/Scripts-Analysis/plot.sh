#!/bin/sh

if [ ! -d plot ]; then
  mkdir plot
fi

files=`ls ../feature_csv_files`

for file in $files; do
  base=`basename $file .csv`
  python3 plot.py ../feature_csv_files/$file plot/$base.png
done