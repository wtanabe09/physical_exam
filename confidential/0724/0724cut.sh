#! /bin/sh

# chose a person "a or b or c"

if [ ! -d cut_videos ]; then
    mkdir cut_videos
fi

# file name example a_001_手首.mp4
names=(
    "挨拶"
    "手首"
    "目"
    "鎖骨"
    "リンパ節"
    "甲状腺1"
    "甲状腺2"
    "喉聴診1"
    "喉聴診2"
    "目反射"
    "輻輳反射1"
    "輻輳反射2"
    "眼球運動"
    "胸部聴診"
    "肺聴診"
    "背中聴診"
    "両手並行"
)

times=(
    "22452300"
    "23002330"
    "29312945"
    "37293738"
    "42364405"
    "44114436"
    "45104546"
    "51025118"
    "52185238"
    "54025427"
    "58345845"
    "58465853"
    "59356004"
    "79408039"
    "88008848"
    "88588940"
    "95219532"
)


let i=0;
for time in ${times[@]}; do
    padding_i="00${i}"
    python3 0724cut.py $time "b_${padding_i-3}_${names[i]}"
    let i++;
done