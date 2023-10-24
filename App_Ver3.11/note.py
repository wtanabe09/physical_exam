import tkinter as tk
from tkinter import filedialog
import cv2 as cv
from PIL import ImageTk, Image
import os
import time
import numpy as np
import math

class Application(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        # time.sleep(5)
        self.iDir = os.path.abspath(os.path.dirname(__file__))
        self.iDirPath = filedialog.askdirectory(initialdir = self.iDir)
        if self.iDirPath == "": 
            exit()
        self.divFile()
        path = self.iDirPath + "/" + self.file_path + "_result.mp4"
        self.video = cv.VideoCapture(path)
        self.fps = int(self.video.get(cv.CAP_PROP_FPS))
        
        self.frameNum = 0
        self.checkVal = 80
        self.file1 = open(self.iDirPath + "/" + self.file_path + "_1.txt", "r")
        self.file2 = open(self.iDirPath + "/" + self.file_path + "_2.txt", "r") 
        self.lines1 = self.file1.readlines()
        self.lines2 = self.file2.readlines()  
        self.num = len(self.lines1)
        self.n = 0   # 手技開始判定値
        self.count = 0
        self.isCounted = True
        
        self.isPose = False
        self.createWidgets()
        self.calc()
        self.play()
        
    def divFile(self):
        self.file_path = ""
        for i in self.iDirPath:
            if i != "/":
                self.file_path += i
            else:
                self.file_path = ""
                
                
        
    def createWidgets(self):
        self.frame1 = tk.Frame(self.root, width="1920" ,height="600")
        self.frame1.propagate(False)
        self.frame1.pack(side="left")
        
        self.frame2 = tk.Frame(self.frame1, width="960", height="600", relief="groove", bd=1)
        self.frame2.propagate(False)
        self.frame2.pack(side="left")
        
        self.frame3 = tk.Frame(self.frame1, width="960", height="600")
        self.frame3.propagate(False)
        self.frame3.pack(side="left")
        
        self.frame4 = tk.Frame(self.frame3, width="960", height="270", relief="solid", bd=1)
        self.frame4.propagate(False)
        self.frame4.pack()
        
        self.frame5 = tk.Frame(self.frame3, width="960", height="330", relief="solid", bd=1)
        self.frame5.propagate(False)
        self.frame5.pack()
        
        self.canvas_video = tk.Canvas(self.frame2, width=960, height=540)
        self.canvas_video.pack()
        
        self.label_title1 = tk.Label(self.frame4, text="手技中の特徴量", font=("nomal", 30, "bold"))
        self.label_title1.pack()
        
        self.label_title2 = tk.Label(self.frame5, text="手技の結果", font=("nomal", 30, "bold"))
        self.label_title2.pack()
        
        self.label_val = tk.Label(self.frame4, text="あいうえお", font=("nomal", 20, "bold"))
        self.label_val.pack()
        
        self.label_val1 = tk.Label(self.frame4, text="「医者」と「患者」の距離：")
        self.label_val1.pack()
        
        self.label_val2 = tk.Label(self.frame4, text="「医者の手」と「患者の顔」の距離：")
        self.label_val2.pack()
        
        self.label_val3 = tk.Label(self.frame4, text="「医者の右手」と「患者の胴体」の距離：")
        self.label_val3.pack()
        
        self.label_val3_2 = tk.Label(self.frame4, text="「医者の右手」と「患者の胴体」の距離：")
        self.label_val3_2.pack()
        
        self.label_val4 = tk.Label(self.frame4, text="患者の肘の角度：")
        self.label_val4.pack()
        
        self.label_res1 = tk.Label(self.frame5, text="「医者」と「患者」の距離\n平均値：\n最大値：\n最小値：")
        self.label_res1.pack()
        
        self.label_res2 = tk.Label(self.frame5, text="「医者の手」と「患者の顔」の距離\n平均値：\n最大値：\n最小値：")
        self.label_res2.pack()
        
        self.label_res3 = tk.Label(self.frame5, text="「医者の右手」と「患者の胴体」の距離\n平均値：\n最大値：\n最小値：")
        self.label_res3.pack()
        
        self.label_res4 = tk.Label(self.frame5, text="「医者の左手」と「患者の胴体」の距離\n平均値：\n最大値：\n最小値：")
        self.label_res4.pack()
        
        self.button_pose = tk.Button(self.frame2, text="一時停止", command=self.pose)
        self.button_pose.pack()
        
    def pose(self):
        self.isPose = not self.isPose
        
    def delWindow(self):
        self.root.destroy()
        
    def play(self):
        start = time.time()
        if not self.isPose:
            self.button_pose["text"] = "一時停止"
            self.frameNum += 1
            ret, debug_image = self.video.read()
            if not ret:
                self.video.set(cv.CAP_PROP_POS_FRAMES, 0)
                self.frameNum = 0
                self.n = 0
                self.count = 0
                self.isCounted = True
            else:
                debug_image = cv.resize(debug_image, (960, 540))
                self.photo_line = ImageTk.PhotoImage(image=Image.fromarray(cv.cvtColor(debug_image, cv.COLOR_BGR2RGB)))
                self.canvas_video.delete("all")
                self.canvas_video.create_image(483, 273, image=self.photo_line)
                self.realCal()
        else:
            self.button_pose["text"] = "再生"
        
        end = time.time()
        if (end - start) < (1/self.fps):
            t = int(((1/self.fps) - (end - start)) * 1000)
        else:
            t = 1
        self.after(t, self.play)
        
    def calc(self):
        notFirst = False
        
        # 平均用変数の初期化
        self.ans1 = []
        self.ans2 = []
        self.ans3 = []
        self.ans4 = []
        
        a1 = []
        a2 = []
        a3 = []
        a4 = []
        
        for i in range(len(self.lines1)):
            # 1患者、2医者
            self.line1 = self.lines2[i].rstrip("\n").split(",")
            self.line2 = self.lines1[i].rstrip("\n").split(",")
            
            # それぞれの行内の要素数を取得
            n = []
            n.append(len(self.line1))
            n.append(len(self.line2))
            # 手技の判定用の座標取得
            hand_r = False; hand_l = False; knee_r = False; knee_l = False
            for j in range(1, n[1], 3):
                # 右手首(15) 左手首(16) 右膝(25) 左膝(26)
                # print("j = ", str(j), ", self.line = ", self.line2[j])
                if int(self.line2[j]) == 15:
                    hand_r = True
                    hand_r_x = self.line2[j+1]
                    hand_r_y = self.line2[j+2]
                elif int(self.line2[j]) == 16:
                    hand_l = True
                    hand_l_x = self.line2[j+1]
                    hand_l_y = self.line2[j+2]
                elif int(self.line2[j]) == 25:
                    knee_r = True
                    knee_r_x = self.line2[j+1]
                    knee_r_y = self.line2[j+2]
                elif int(self.line2[j]) == 26:
                    knee_l = True
                    knee_l_x = self.line2[j+1]
                    knee_l_y = self.line2[j+2]
            
            # 距離計算
            if hand_r and knee_r:
                d1 = np.sqrt((int(hand_r_x) - int(knee_r_x))**2 + (int(hand_r_y) - int(knee_r_y))**2)
                # print(d1)
                if d1 >= self.checkVal:
                    self.n += 1
                else:
                    self.n = 0
                
            # 手技判定
            if self.n >= 1:
                notFirst = True
                
                # 患者の座標
                eye1_r = False; eye1_l = False; shol1_r = False; shol1_l = False; hand1_r = False; hand1_l = False
                for j in range(1, n[0], 3):
                    # 右目(2) 左目(5) 右肩(11) 左肩(12) 右手首(15) 左手首(16) 左肘(14)
                    if int(self.line1[j]) == 2:
                        eye1_r = True
                        eye1_r_x = self.line1[j+1]
                        eye1_r_y = self.line1[j+2]
                    elif int(self.line1[j]) == 5:
                        eye1_l = True
                        eye1_l_x = self.line1[j+1]
                        eye1_l_y = self.line1[j+2]
                    elif int(self.line1[j]) == 11:
                        shol1_r = True
                        shol1_r_x = self.line1[j+1]
                        shol1_r_y = self.line1[j+2]
                    elif int(self.line1[j]) == 12:
                        shol1_l = True
                        shol1_l_x = self.line1[j+1]
                        shol1_l_y = self.line1[j+2]
                    elif int(self.line1[j]) == 14:
                        elbow1_l_x = True
                        elbow1_l_x = self.line1[j+1]
                        elbow1_l_y = self.line1[j+2]
                    elif int(self.line1[j]) == 15:
                        hand1_r = True
                        hand1_r_x = self.line1[j+1]
                        hand1_r_y = self.line1[j+2]
                    elif int(self.line1[j]) == 16:
                        hand1_l = True
                        hand1_l_x = self.line1[j+1]
                        hand1_l_y = self.line1[j+2]
                        
                # 医者の座標
                shol2_r = False; shol2_l = False; hand2_r = False; hand2_l = False
                for j in range(1, n[1], 3):
                    # 右肩(11) 左肩(12) 右手首(15) 左手首(16)
                    if int(self.line2[j]) == 11:
                        shol2_r = True
                        shol2_r_x = self.line2[j+1]
                        shol2_r_y = self.line2[j+2]
                    elif int(self.line2[j]) == 12:
                        shol2_l = True
                        shol2_l_x = self.line2[j+1]
                        shol2_l_y = self.line2[j+2]
                    elif int(self.line2[j]) == 15:
                        hand2_r = True
                        hand2_r_x = self.line2[j+1]
                        hand2_r_y = self.line2[j+2]
                    elif int(self.line2[j]) == 16:
                        hand2_l = True
                        hand2_l_x = self.line2[j+1]
                        hand2_l_y = self.line2[j+2]
                # このインデントが1フレームごとの処理
                # 特徴量1
                if shol1_l and shol2_r:
                    a1.append(abs(int(shol2_r_x) - int(shol1_l_x)))
                        
                # 特徴量2
                if eye1_l and hand2_r:
                    a2.append(abs(int(eye1_l_x) - int(hand2_r_x)))
                    
                if shol1_l and hand2_r:
                    a3.append(abs(int(shol1_l_x) - int(hand2_r_x)))
                    
                if shol1_l and hand2_l:
                    a4.append(abs(int(shol1_l_x) - int(hand2_l_x)))
            else:
                if notFirst:
                    if len(a1) != 0:
                        self.ans1.append([sum(a1) / len(a1), max(a1), min(a1)])
                    if len(a2) != 0:
                        self.ans2.append([sum(a2) / len(a2), max(a2), min(a2)])
                    if len(a3) != 0:
                        self.ans3.append([sum(a3) / len(a3), max(a3), min(a3)])
                    if len(a4) != 0:
                        self.ans4.append([sum(a4) / len(a4), max(a4), min(a4)])
                    
                    a1 = []; a2 = []; a3 = []; a4 = []
                    
        if len(a1) != 0:
            self.ans1.append([sum(a1) / len(a1), max(a1), min(a1)])
        if len(a2) != 0:
            self.ans2.append([sum(a2) / len(a2), max(a2), min(a2)])
        if len(a3) != 0:
            self.ans3.append([sum(a3) / len(a3), max(a3), min(a3)])
        if len(a4) != 0:
            self.ans4.append([sum(a4) / len(a4), max(a4), min(a4)])
        
        # print(self.ans1)
        # print(self.ans2)
        # print(self.ans3)
        # print(self.ans4)
        # 初期化
        self.n = 0
        self.count = 0
        hand_r = False; hand_l = False; knee_r = False; knee_l = False
                
    def realCal(self):
        # 1患者、2医者
        self.line1 = self.lines2[self.frameNum-1].rstrip("\n").split(",")
        self.line2 = self.lines1[self.frameNum-1].rstrip("\n").split(",")
        
        # それぞれの行内の要素数を取得
        n = []
        n.append(len(self.line1))
        n.append(len(self.line2))
        
        # 手技の判定用の座標取得
        hand_r = False; hand_l = False; knee_r = False; knee_l = False
        
        for j in range(1, n[1], 3):
            # 左手首(15) 右手首(16) 右膝(25) 左膝(26)
            # print("j = ", str(j), ", self.line = ", self.line2[j])
            if int(self.line2[j]) == 15:
                hand_r = True
                hand_r_x = self.line2[j+1]
                hand_r_y = self.line2[j+2]
            elif int(self.line2[j]) == 16:
                hand_l = True
                hand_l_x = self.line2[j+1]
                hand_l_y = self.line2[j+2]
            elif int(self.line2[j]) == 25:
                knee_r = True
                knee_r_x = self.line2[j+1]
                knee_r_y = self.line2[j+2]
            elif int(self.line2[j]) == 26:
                knee_l = True
                knee_l_x = self.line2[j+1]
                knee_l_y = self.line2[j+2]
        
        # 距離計算
        if hand_r and knee_r:
            d1 = np.sqrt((int(hand_r_x) - int(knee_r_x))**2 + (int(hand_r_y) - int(knee_r_y))**2)
            if d1 >= self.checkVal:
                self.n += 1
            else:
                self.n = 0
            
        # 手技判定
        if self.n >= 1:
            if self.isCounted:
                self.isCounted = False
            # 特徴量計算
            self.label_val["text"] = "手技{}".format(self.count + 1)
            self.label_val["fg"] = "red"
            
            self.label_title2["text"] = "手技{}の結果".format(self.count + 1)
            
            # 0.5sec
            if self.n % 10 == 0:
                # 患者の座標
                eye1_r = False; eye1_l = False; shol1_r = False; shol1_l = False; hand1_r = False; hand1_l = False
                for j in range(1, n[0], 3):
                    # 右目(2) 左目(5) 右肩(11) 左肩(12) 右手首(15) 左手首(16) 左肘(14)
                    if int(self.line1[j]) == 2:
                        eye1_r = True
                        eye1_r_x = self.line1[j+1]
                        eye1_r_y = self.line1[j+2]
                    elif int(self.line1[j]) == 5:
                        eye1_l = True
                        eye1_l_x = self.line1[j+1]
                        eye1_l_y = self.line1[j+2]
                    elif int(self.line1[j]) == 11:
                        shol1_r = True
                        shol1_r_x = self.line1[j+1]
                        shol1_r_y = self.line1[j+2]
                    elif int(self.line1[j]) == 12:
                        shol1_l = True
                        shol1_l_x = self.line1[j+1]
                        shol1_l_y = self.line1[j+2]
                    elif int(self.line1[j]) == 14:
                        elbow1_l = True
                        elbow1_l_x = self.line1[j+1]
                        elbow1_l_y = self.line1[j+2]
                    elif int(self.line1[j]) == 15:
                        hand1_r = True
                        hand1_r_x = self.line1[j+1]
                        hand1_r_y = self.line1[j+2]
                    elif int(self.line1[j]) == 16:
                        hand1_l = True
                        hand1_l_x = self.line1[j+1]
                        hand1_l_y = self.line1[j+2]
                        
                # 医者の座標
                shol2_r = False; shol2_l = False; hand2_r = False; hand2_l = False
                for j in range(1, n[1], 3):
                    # 右肩(11) 左肩(12) 右手首(15) 左手首(16)
                    if int(self.line2[j]) == 11:
                        shol2_r = True
                        shol2_r_x = self.line2[j+1]
                        shol2_r_y = self.line2[j+2]
                    elif int(self.line2[j]) == 12:
                        shol2_l = True
                        shol2_l_x = self.line2[j+1]
                        shol2_l_y = self.line2[j+2]
                    elif int(self.line2[j]) == 15:
                        hand2_r = True
                        hand2_r_x = self.line2[j+1]
                        hand2_r_y = self.line2[j+2]
                    elif int(self.line2[j]) == 16:
                        hand2_l = True
                        hand2_l_x = self.line2[j+1]
                        hand2_l_y = self.line2[j+2]
                        
                # 特徴量1
                if shol1_l and shol2_r:
                    self.label_val1["text"] = "「医者」と「患者」の距離：{}".format(abs(int(shol2_r_x) - int(shol1_l_x)))
                else:
                    self.label_val1["text"] = "「医者」と「患者」の距離："
                        
                # 特徴量2
                if eye1_l and hand2_r:
                    self.label_val2["text"] = "「医者の手」と「患者の顔」の距離：{}".format(abs(int(eye1_l_x) - int(hand2_r_x)))
                else:
                    self.label_val2["text"] = "「医者の手」と「患者の顔」の距離："
                    
                if shol1_l and hand2_r:
                    self.label_val3["text"] = "「医者の右手」と「患者の胴体」の距離：{}".format(abs(int(shol1_l_x) - int(hand2_r_x)))
                else:
                    self.label_val3["text"] = "「医者の右手」と「患者の胴体」の距離："
                    
                if shol1_l and hand2_l:
                    self.label_val3_2["text"] = "「医者の左手」と「患者の胴体」の距離：{}".format(abs(int(shol1_l_x) - int(hand2_l_x)))
                else:
                    self.label_val3_2["text"] = "「医者の左手」と「患者の胴体」の距離："
                        
                # 特徴量3
                if shol1_l and elbow1_l and hand1_l:
                    shoulder = np.array([int(shol1_l_y), int(shol1_l_x)])
                    elbow = np.array([int(elbow1_l_y), int(elbow1_l_x)])
                    hand = np.array([int(hand1_l_y), int(hand1_l_x)])
                    deg = self.calculate_elbow_angle(shoulder, elbow, hand)
                    self.label_val4["text"] = "患者の肘の角度：{:.2f}度".format(deg)
                else:
                    self.label_val4["text"] = "患者の肘の角度："
                    
                # 結果表示
                self.label_res1["text"] = "「医者」と「患者」の距離\n平均値：{:.2f}\n最大値：{}\n最小値：{}".format(self.ans1[self.count][0], self.ans1[self.count][1], self.ans1[self.count][2])
                self.label_res2["text"] = "「医者の手」と「患者の顔」の距離\n平均値：{:.2f}\n最大値：{}\n最小値：{}".format(self.ans2[self.count][0], self.ans2[self.count][1], self.ans2[self.count][2])
                self.label_res3["text"] = "「医者の右手」と「患者の胴体」の距離\n平均値：{:.2f}\n最大値：{}\n最小値：{}".format(self.ans3[self.count][0], self.ans3[self.count][1], self.ans3[self.count][2])
                self.label_res4["text"] = "「医者の左手」と「患者の胴体」の距離\n平均値：{:.2f}\n最大値：{}\n最小値：{}".format(self.ans4[self.count][0], self.ans4[self.count][1], self.ans4[self.count][2])
        else:
            if not self.isCounted:
                self.count += 1
                self.isCounted = True
            
            self.label_val["text"] = "手技外"
            self.label_val["fg"] = "blue"
            
            # クリア
            self.label_val1["text"] = "「医者」と「患者」の距離："
            self.label_val2["text"] = "「医者の手」と「患者の顔」の距離："
            self.label_val3["text"] = "「医者の右手」と「患者の胴体」の距離："
            self.label_val3_2["text"] = "「医者の左手」と「患者の胴体」の距離："
            self.label_val4["text"] = "患者の肘の角度："
            
            self.label_res1["text"] = "「医者」と「患者」の距離\n平均値：\n最大値：\n最小値："
            self.label_res2["text"] = "「医者の手」と「患者の顔」の距離\n平均値：\n最大値：\n最小値："
            self.label_res3["text"] = "「医者の手」と「患者の胴体」の距離\n平均値：\n最大値：\n最小値："
            self.label_res4["text"] = "「医者の左手」と「患者の胴体」の距離\n平均値：\n最大値：\n最小値："
            
            self.label_title2["text"] = "手技の結果"
                
            
    def calculate_elbow_angle(self, shoulder, elbow, hand):
        # 肩から肘へのベクトル
        shoulder_to_elbow = shoulder - elbow
        
        # 肘から手へのベクトル
        elbow_to_hand = elbow - hand
        
        # ベクトルの内積を計算
        dot_product = np.dot(shoulder_to_elbow, elbow_to_hand)
        
        # ベクトルの大きさを計算
        norm_shoulder_to_elbow = np.linalg.norm(shoulder_to_elbow)
        norm_elbow_to_hand = np.linalg.norm(elbow_to_hand)
        
        # ベクトルの内積から角度を計算（ラジアン）
        cos_theta = dot_product / (norm_shoulder_to_elbow * norm_elbow_to_hand)
        angle_radians = np.arccos(np.clip(cos_theta, -1.0, 1.0))
        
        # ラジアンから度に変換
        angle_degrees = np.degrees(angle_radians)
        
        return 180 - angle_degrees
                
        
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1980x1080")
    root.title("録画解析")
    
    app = Application(root)
    app.mainloop()
