#! /bin/sh

if [ ! -d cut_videos ]; then
    mkdir cut_videos
fi

times=(
    "19001910"
    "20202033"
    "21412200"
)

names=("手首1" "手首2" "手首3")

# echo ${times[0]}
# echo ${names[0]}

let i=0;
for time in ${times[@]}; do
    echo "${i}  ${time}"
    echo "${i}  ${names[i]}"
    python3 0724cut.py $time "${i}_${names[i]}"
    let i++;
done