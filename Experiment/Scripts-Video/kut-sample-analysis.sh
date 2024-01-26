#!/bin/sh

video_files=`ls ../kut-sample-video/*.mp4`

for video_file in $video_files; do
    base_file=`basename $video_file .mp4`
    # python3 movie_edit_coordinate_outpu.py input_video output_csv output_video role_num
    #python3 add_header_to_csv.py input_csv fps
    echo movie_edit_coordinate_output.py add_header $base_file -1
    python3 movie_edit_coordinate_output.py ../kut-sample-video/$video_file ../kut-sample-video/data_csv_files/$base_file-1.csv ../kut-sample-video/data_video_files/$base_file-1.mp4 1
    python3 ../Scripts-Csv/add_header_to_csv.py ../kut-sample-video/data_csv_files/$base_file-1.csv 30
    
    echo movie_edit_coordinate_output add_header $base_file -2
    python3 movie_edit_coordinate_output.py ../kut-sample-video/$video_file ../kut-sample-video/data_csv_files/$base_file-2.csv ../kut-sample-video/data_video_files/$base_file-2.mp4 2
    python3 ../Scripts-Csv/add_header_to_csv.py ../kut-sample-video/data_csv_files/$base_file-2.csv 30
done