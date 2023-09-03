#!/bin/bash

if [ ! -d crop ]; then
    mkdir crop
fi
if [ ! -d images ]; then
    mkdir images
fi

files="b_000_挨拶.mp4
b_0010_輻輳反射1.mp4
b_0011_輻輳反射2.mp4
b_0012_眼球運動.mp4
b_0013_胸部聴診.mp4
b_0014_肺聴診.mp4
b_0015_背中聴診.mp4
b_0016_両手並行.mp4
b_0017_通し.mp4
b_001_手首.mp4
b_002_目.mp4
b_003_鎖骨.mp4
b_004_リンパ節.mp4
b_005_甲状腺1.mp4
b_006_甲状腺2.mp4
b_007_喉聴診1.mp4
b_008_喉聴診2.mp4
b_009_目反射.mp4
c_000_挨拶.mp4
c_0010_輻輳反射2.mp4
c_0011_眼球運動.mp4
c_0012_胸部聴診.mp4
c_0013_肺聴診.mp4
c_0014_背中聴診.mp4
c_0015_通し.mp4
c_001_手首.mp4
c_002_リンパ節.mp4
c_003_甲状腺.mp4
c_004_喉聴診1.mp4
c_005_喉聴診2.mp4
c_006_喉聴診3.mp4
c_007_目反射1.mp4
c_008_目反射2.mp4
c_009_輻輳反射1.mp4
"
for mp4 in $files; do
    base=`basename $mp4 .mp4`
    echo mp4:$mp4 base:$base
    # ffmpeg -i $mp4 -vf crop=w=960:h=540:x=0:y=0   crop/$base-R.mp4
    ffmpeg -i $mp4 -vf crop=w=320:h=180:x=320:y=0 crop/$base-L.mp4
    ffmpeg -i $mp4 -vf crop=w=320:h=180:x=0:y=180 crop/$base-C.mp4
    # ffmpeg -i crop/$base-R.mp4 -r 1 images/$base-R-%03d.jpg
    ffmpeg -i crop/$base-L.mp4 -r 1 images/$base-L-%03d.jpg
    ffmpeg -i crop/$base-C.mp4 -r 1 images/$base-C-%03d.jpg
done