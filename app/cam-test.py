import cv2

def main():
    # カメラのキャプチャを開始 (0はデフォルトのカメラを指す)
    cap = cv2.VideoCapture(6)

    if not cap.isOpened():
        print("カメラが開けませんでした。")
        return

    try:
        while True:
            # カメラからフレームを読み取る
            ret, frame = cap.read()
            if not ret:
                print("フレームを読み込めませんでした。")
                break

            # フレームを表示
            cv2.imshow('Camera Feed', frame)

            # 'q'キーが押されたらループを終了
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        # カメラとウィンドウを閉じる
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

