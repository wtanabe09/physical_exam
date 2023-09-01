import ffmpeg
import re

def get_camera_list():
    # エラー内容をffmpeg_outputに代入。ffmpegの実行結果は常にエラー。
    try:
        # dummy: Input/output error
        ffmpeg_output = ffmpeg.input('dummy', format='avfoundation', list_devices='true').output('dummy').run(capture_stderr=True).decode('utf8')
    except ffmpeg.Error as e: 
        ffmpeg_output = e.stderr.decode('utf8')

    # ffmpegのエラー内容から、カメラデバイス名を抽出。
    regex_specified_range = "AVFoundation video devices:.*?Capture screen 0"
    regex_target_to_remove = "\[AVFoundation indev @.*?\]"
    extracted_lists = re.findall(regex_specified_range, re.sub(regex_target_to_remove, "", ffmpeg_output), flags=re.DOTALL)
    return  [s for s in extracted_lists[0].split('\n') if ("AVFoundation video devices:" not in s) and ("Capture screen 0" not in s)]

def main():
    # カメラデバイスの一覧を出力。
    for camera in get_camera_list():
        print(camera)

if __name__ == "__main__":
    main() 

