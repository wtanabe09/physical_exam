#!/bin/sh

input=$@ # ../0724cut_videos/*.mp4
files=`ls $input`

for file in $files; do
  base=`basename $file .mp4`
  dir=`dirname $file`
  python3 coordinate_output.py "${file}" "${dir}/point_csv/${base}.csv"
done

echo prosess is done
