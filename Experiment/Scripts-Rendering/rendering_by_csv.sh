#!/bin/sh

# datadir='../Fixdata-Analysis'
# dirs=`ls -d ../Fixdata-Analysis/*2023*`
datadir='../kut-sample-video'
dirs=`ls -d $datadir/*.mp4`

for dir in $dirs; do
    echo $dir
    timestamp=`basename $dir .mp4`
    echo $timestamp
    python3 rendering_by_csv.py $timestamp $datadir $datadir/data_csv_files $datadir/feature_csv_files $datadir/rendering_images_videos
done

echo rendering done


# datadir='../Fixdata-Analysis'
# dirs=`ls -d ../Fixdata-Analysis/*2023*`
# # datadir='../kut-sample-video'
# # dirs=`ls -d $datadir/*.mp4`

# for dir in $dirs; do
#     echo $dir
#     timestamp=`basename $dir .mp4`
#     python3 rendering_by_csv.py $timestamp $datadir/videos $datadir/data_csv_files $datadir/feature_csv_files $datadir/rendering_images_videos
# done

# echo rendering done