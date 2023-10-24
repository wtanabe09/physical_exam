#特徴量表示動画作成
import cv2
import sys
import calculation # 自作 calculation.py


file_base = sys.argv[1]
input_file = './crop/'+file_base+'-C.mp4'
window_name = 'display'
cap = cv2.VideoCapture(input_file)

video_fps = cap.get(cv2.CAP_PROP_FPS)
video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))    
video_hight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
size = (video_width, video_hight)
fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
writer = cv2.VideoWriter('./feature_video/'+file_base+'-C_feature.mp4', fmt, video_fps, size)

dist = calculation.calc_distance(file_base)
int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(dist[0])
print(f'fps: {video_fps}')
print(f'num of frame: {cap.get(cv2.CAP_PROP_FRAME_COUNT)}')

i = 0
count = 0
n = 0
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print('video end')
        break
    # 字幕表示
    if dist[i] <= 0.12:
        n += 1
        # print(dist[i])
    else:
        n = 0

    if n >= 60:
        color = (255, 0, 0)
        # text = 'Not process'
    else:
        color = (255, 255, 255)
        # text = 'In process'
        
    cv2.putText(frame, f'{dist[i]}', (0, 35), \
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, thickness=2)
    
    writer.write(frame)
    i += 1

cap.release()
writer.release()
cv2.destroyWindow(window_name)