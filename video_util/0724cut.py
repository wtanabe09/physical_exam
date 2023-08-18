# 動画を指定した開始，終了秒でカットするPythonプログラム
# カットしたい時間をあらかじめ調べておく必要がある

import os
import sys
import datetime
os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/local/bin/ffmpeg"


td_start = datetime.timedelta(weeks=0, days=0, hours=0, minutes=int(sys.argv[1][0:2]), seconds=int(sys.argv[1][2:4]), milliseconds=0, microseconds=0)
start_seconds = td_start.seconds
td_end = datetime.timedelta(weeks=0, days=0, hours=0, minutes=int(sys.argv[1][4:6]), seconds=int(sys.argv[1][6:8]), milliseconds=0, microseconds=0)
end_seconds = td_end.seconds

from moviepy.editor import *
# 編集したい動画のパスを指定し、カットする開始秒と終了秒を指定。
video = VideoFileClip("./0724video.mp4").subclip(start_seconds, end_seconds)

# 編集した動画を保存するパスを指定
video.write_videofile(f'./cut_videos/{sys.argv[2]}.mp4',fps=29)
