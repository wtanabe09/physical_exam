#!/bin/sh

for file in "$@"; do
    basename=`expr "$file" : '\(.*\)\.mp4'`
    ffmpeg -i $file \
	   -vf crop=w=960:h=540:x=0:y=0 ${basename}_1.mp4 \
	   -vf crop=w=960:h=540:x=960:y=0 ${basename}_2.mp4 \
	   -vf crop=w=960:h=540:x=1920:y=0 ${basename}_3.mp4 \
	   -vf crop=w=960:h=540:x=0:y=540 ${basename}_4.mp4 \
	   -vf crop=w=960:h=540:x=960:y=540 ${basename}_5.mp4 \
	   > $basename.crop.log 2>&1
done