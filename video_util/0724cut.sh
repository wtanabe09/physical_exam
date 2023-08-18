#! /bin/sh

if [ ! -d cut_videos ]; then
    mkdir cut_videos
fi

times=(
    "19001910"
    "20202033"
    "21412200"
)

# file_name: studentId_procedure, output_file_name: id_studentId_procedure
names=("a_手首1" "a_手首2" "a_手首3")

# echo ${times[0]}
# echo ${names[0]}

let i=0;
for time in ${times[@]}; do
    echo "${i}  ${time}"
    echo "${i}  ${names[i-1]}"
    padding_i="00${i}"
    echo "${padding_i:-3}"
    python3 0724cut.py $time "${padding_i:-3}_${names[i]}"
    let i++;
done