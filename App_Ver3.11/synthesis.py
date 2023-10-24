import cv2
import sys


def comp(name):
    # 動画のパスを指定
    video1_path = "./" + name + "_motion1.mp4"
    video2_path = "./" + name + "_motion2.mp4"

    # ファイルを読み込み
    cap1 = cv2.VideoCapture(video1_path)
    cap2 = cv2.VideoCapture(video2_path)

    # 入力動画からフレームの幅と高さを取得
    frame_width = int(cap1.get(3))
    frame_height = int(cap1.get(4))
    input_fps = int(cap1.get(cv2.CAP_PROP_FPS))

    # 出力動画の設定
    # filename = name + "_motion.mp4"
    filename = name + "_result.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 使用するコーデック
    out = cv2.VideoWriter(filename, fourcc, input_fps, (960, 540))

    # 出力する動画のサイズを指定
    width = 960
    height = 540

    # 動画を再生する
    while True:
        # 1つ目の動画から1フレーム取得する
        ret1, frame1 = cap1.read()
        if not ret1:
            break

        # 2つ目の動画から1フレーム取得する
        ret2, frame2 = cap2.read()
        if not ret2:
            break

        # フレームのサイズを合わせる
        frame1 = cv2.resize(frame1, (width, height))
        frame2 = cv2.resize(frame2, (width, height))

        # 画像を重ね合わせる
        frame3 = cv2.addWeighted(
            src1=frame1, alpha=0.5,
            src2=frame2, beta=0.5,
            gamma=0
        )

        # 画像を表示する
        out.write(frame3)

    # 終了時処理
    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    comp("2023090416193736489")