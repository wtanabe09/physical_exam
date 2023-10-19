#!/bin/sh

files=`ls 5-cam-video`

for file in $files; do
    base=`basename $file .mp4`
    python3 ../../budge-mediapipe/coordinate_output.py "5-cam-video/${file}" "${base}.csv"
    echo "created ${file}"
done