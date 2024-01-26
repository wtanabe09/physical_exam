#!/bin/sh

files=(
    "2_a_20231103103438865789"
    "2_c_20231103110821339674"
    "3_a_20231103104605959603"
    "4_a_20231103104818182554"
    "6_c_20231103110920094980"
)

for file in ${files[@]}; do
    # cp "${file}/${file}_1.csv" "data_csv_files/${file}_1.csv"
    # cp "${file}/${file}_2.csv" "data_csv_files/${file}_2.csv"

    # add_header.py input_path output_path
    python3 add_header.py "${file}/${file}_1.csv" "data_csv_files/${file}-1.csv"
    python3 add_header.py "${file}/${file}_2.csv" "data_csv_files/${file}-2.csv"
    echo cp done $file
done