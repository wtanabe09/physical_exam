#!/bin/sh

files=`ls data_csv_files/*-doc.csv`

for file in $files; do
    base=`basename $file -doc.csv`
    mkdir "data_csv_files/${base}"
    mv "data_csv_files/${base}-doc.csv" "data_csv_files/${base}-pat.csv" "data_csv_files/${base}/."
done