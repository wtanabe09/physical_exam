#!/bin/sh

# input=$@ # clop
files=`ls ./crop_videos/b*-C.mp4`
echo $files
for file in $files; do
  base=`basename $file .mp4`
  echo $base
  python3 coordinate_output.py "./crop_videos/${base}.mp4" "./point_csv/${base}.csv"
done

echo prosess is done
