# 動画を指定した開始，終了秒でカットするPythonプログラム
# カットしたい時間をあらかじめ調べておく必要がある
# sh 0724cut.py inputfile start_minites_seconds_end_minutes_seconds outputfile
# sh 0724cut.py 2023-11-03-11-29-35.mp4 02300422 2023110311320552.mp4

import os
import sys
import datetime
from moviepy.editor import *
os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/local/bin/ffmpeg"

input_file = sys.argv[1]

td_start = datetime.timedelta(weeks=0, days=0, hours=0, minutes=int(sys.argv[2][0:2]), seconds=int(sys.argv[2][2:4]), milliseconds=0, microseconds=0)
start_seconds = td_start.seconds
td_end = datetime.timedelta(weeks=0, days=0, hours=0, minutes=int(sys.argv[2][4:6]), seconds=int(sys.argv[2][6:8]), milliseconds=0, microseconds=0)
end_seconds = td_end.seconds

# 編集したい動画のパスを指定し、カットする開始秒と終了秒を指定。
video = VideoFileClip(input_file).subclip(start_seconds, end_seconds)

# 編集した動画を保存するパスを指定
video.write_videofile(f'./cut_videos/{sys.argv[3]}',fps=29)
