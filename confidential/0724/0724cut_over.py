# 動画を指定した開始，終了秒でカットするPythonプログラム
# カットしたい時間をあらかじめ調べておく必要がある
# 0724cut.pyは100分を超えたものに対応していないため，100分以上のものはとりあえず，手動で対応する．

import os
# import sys
import datetime
os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/bin/ffmpeg"


td_start = datetime.timedelta(weeks=0, days=0, hours=0, minutes=106, seconds=21, milliseconds=0, microseconds=0)
start_seconds = td_start.seconds
td_end = datetime.timedelta(weeks=0, days=0, hours=0, minutes=113, seconds=53, milliseconds=0, microseconds=0)
end_seconds = td_end.seconds

from moviepy.editor import *
# 編集したい動画のパスを指定し、カットする開始秒と終了秒を指定。
video = VideoFileClip("./0724video.mp4").subclip(start_seconds, end_seconds)

# 編集した動画を保存するパスを指定
video.write_videofile(f'./cut_videos/c_0015_通し.mp4',fps=29)
