#!/bin/sh

files=`ls 5-cam-video`

for file in $files; do
    python3 ../../budge-mediapipe/coordinate_output.py "5-cam-video/${file}" "./${file##*}.csv"
done