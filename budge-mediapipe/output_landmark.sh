#!/bin/sh

files=`ls ../input_files`
echo $files

for file in $files; do
  python3 analysis.py `../$file`
done

echo prosess is done
