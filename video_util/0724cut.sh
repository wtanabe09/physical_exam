#! /bin/sh

# chose a person "a or b or c"

if [ ! -d cut_videos ]; then
    mkdir cut_videos
fi

# file name example a_001_手首.mp4
names=(
    "手首1"
    "手首2"
    "手首3"
)

times=(
    "19001910"
    "20202033"
    "21412200"
)


let i=0;
for time in ${times[@]}; do
    padding_i="00${i}"
    python3 0724cut.py $time "a_${padding_i-3}_${names[i]}"
    let i++;
done