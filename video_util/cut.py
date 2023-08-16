# 動画を指定した開始，終了秒でカットするPythonプログラム
# カットしたい時間をあらかじめ調べておく必要がある

import os
os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"

from moviepy.editor import *
# 編集したい動画のパスを指定し、カットする開始秒と終了秒を指定。
video = VideoFileClip("target_file_path").subclip(5, 10)

# 編集した動画を保存するパスを指定
video.write_videofile("out_put_file_path",fps=29)
