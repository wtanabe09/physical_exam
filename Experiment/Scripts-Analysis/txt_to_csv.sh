# 各結果のディレクトリにあるtxtファイルcsvに変換し，data_csv_filesディレクトリに移動する．
# cp-csv.sh：csvファイルを作り直したものはこちらを利用する.（ヘッダーの追加したものを指定場所に作成）


#!/bin/sh

if [ ! -d data_csv_files ]; then
  mkdir data_csv_files
fi

parent=$@  # Result_chair or Result_bed の相対パスをコマンドライン引数で指定 (./)
dirs=`ls -d $parent *2023*`

# ディレクトリ名とファイル名が同名であることが前提
for dir in $dirs; do
  python3 txt_to_csv.py "${dir}/${dir}_1.txt" "data_csv_files/${dir}-1.csv"
  python3 txt_to_csv.py "${dir}/${dir}_2.txt" "data_csv_files/${dir}-2.csv"
  echo "create ${dir}"
done

echo 'txt_to_csv done'

echo 'add-header cp-csv start'
files=(
    "2_a_20231103103438865789"
    "2_c_20231103110821339674"
    "3_a_20231103104605959603"
    "4_a_20231103104818182554"
    "6_c_20231103110920094980"
)

for file in ${files[@]}; do
    # add_header.py input_path output_path
    python3 add_header.py "${file}/${file}_1.csv" "data_csv_files/${file}-1.csv"
    python3 add_header.py "${file}/${file}_2.csv" "data_csv_files/${file}-2.csv"
    echo add header cp done $file
done