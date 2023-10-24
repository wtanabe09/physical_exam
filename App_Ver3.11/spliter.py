import cv2

def videoTrim(name):
    for i in range(1, 6, 1):
        # 入力動画ファイル名と出力動画ファイル名
        input_video_path = name + ".mp4"
        output_video_path = name + "_" + str(i) + ".mp4"

        # トリミング後の幅と高さ
        output_width = 960
        output_height = 540
        
        x_start = 960 * ((i-1)%3)
        x_end = 960 * ((i-1)%3+1) - 1
        
        if i <= 3:
            y_start = 0
            y_end = 539
        else:
            y_start = 540
            y_end = 1079

        # 入力動画のキャプチャを開く
        cap = cv2.VideoCapture(input_video_path)

        # 入力動画からフレームの幅と高さを取得
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        input_fps = int(cap.get(cv2.CAP_PROP_FPS))

        # 出力動画の設定
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 使用するコーデック
        out = cv2.VideoWriter(output_video_path, fourcc, input_fps, (output_width, output_height))

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # トリミングとリサイズ
            frame = frame[y_start:y_end, x_start:x_end]
            frame = cv2.resize(frame, (output_width, output_height))

            # 出力動画にフレームを書き込む
            frame = cv2.flip(frame, 1)
            out.write(frame)

        # リソースの解放
        cap.release()
        out.release()

        print("動画のトリミングとリサイズが完了しました。")

# if __name__ == "__main__":
#     videoTrim("2023090322402928262")