#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import argparse
import cv2 as cv
import numpy as np
import mediapipe as mp
from PIL import Image, ImageTk, ImageOps  # 画像データ用
from utils import CvFpsCalc
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import threading
import datetime
import time
import spliter
import render
import os
import synthesis

REC = False

class Application(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.pack()
        self.pack_propagate(0)
        self.on = True
        self.line = True
        self.x_start = 0; self.x_end = 959; self.y_start = 0; self.y_end = 539
        self.num = 0
        self.isRec = False
        self.isRec2 = False
        self.REC = False
        self.choseCamNumber = 8  # ここに使用するカメラの番号を入力 ####################
        self.createWidgets()
        self.main()
        self.update()
    
    def isPlay(self):
        self.on = not self.on
        
    def isLine(self):
        self.line = not self.line
        
    def changeCam(self):
        self.num += 1
        self.x_start = 960 * ((self.num-1)%3)
        self.x_end = 960 * ((self.num-1)%3+1) - 1
        
        if self.num <= 3:
            self.y_start = 0
            self.y_end = 539
        else:
            self.y_start = 540
            self.y_end = 1079
        
        if self.num >= 5:
            self.num = 0
            
    def rec(self):
        self.REC = not self.REC
        if self.REC:
            self.thread1 = threading.Thread(target=self.t1)
            print("ok")
            self.thread1.start()
            self.button_rec["text"] = "録画停止"
            self.button_rec["fg"] = "red"
        else:
            self.button_rec["text"] = "録画開始"
            self.button_rec["fg"] = "blue"
            messagebox.showinfo("処理中", "しばらくお待ち下さい。")
            time.sleep(1)
            spliter.videoTrim(self.name)
            time.sleep(1)
            render.main(self.name, self.file_time, 1)
            render.main(self.name, self.file_time, 2)
            synthesis.comp(self.name)
            os.system("mkdir " + self.name)
            os.system("mv " + self.name + "*.mp4 ./" + self.name + "/")
            os.system("mv " + self.name + "*.txt ./" + self.name + "/")
            os.system("sh analysis.sh " + self.name + "/")
            messagebox.showinfo("完了", "処理が完了しました。")
            
    def win2(self):
        # self.newWindow = tk.Toplevel(self.root)
        # self.app = Application2(self.newWindow)
        # self.app.mainloop()
        os.system("python3 note.py &")
        
    def createWidgets(self):
        self.canvas = tk.Canvas(self.root, width=960, height=540, bg="black")
        self.canvas.pack(side="top")
        
        self.frame_buttons = tk.Frame(self.root)
        self.frame_buttons.pack()
        
        self.button_on_off = tk.Button(self.frame_buttons, text="一時停止", command=self.isPlay)
        self.button_on_off.pack(side="left")
        
        self.button_change_cam = tk.Button(self.frame_buttons, text="カメラ移動", command=self.changeCam)
        self.button_change_cam.pack(side="left")
        
        self.button_line = tk.Button(self.frame_buttons, text="姿勢表示", command=self.isLine)
        self.button_line.pack(side="left")
        
        self.button_rec = tk.Button(self.frame_buttons, text="録画開始", fg="blue", command=self.rec)
        self.button_rec.pack(side="left")
        
        self.button_analyse = tk.Button(self.frame_buttons, text="録画解析", command=self.win2)
        self.button_analyse.pack(side="left")
        
        self.button_close = tk.Button(self.frame_buttons, text="閉じる", command=exit)
        self.button_close.pack(side="left")
        
        self.label_text = tk.Label(self.root, pady=10, text="録画開始ボタンはカメラ5台分の映像を同時に録画します。")
        self.label_text.pack()
        
        self.label_position = tk.Label(self.root, text="ここに")
        # self.label_position.pack()
    
    # デバイスの情報を取得
    def get_args(self):
        parser = argparse.ArgumentParser()

        parser.add_argument("--device", type=int, default=self.choseCamNumber)
        parser.add_argument("--width", help='cap width', type=int, default=2880)
        parser.add_argument("--height", help='cap height', type=int, default=1080)

        # parser.add_argument('--upper_body_only', action='store_true')  # 0.8.3 or less
        parser.add_argument("--model_complexity",
                            help='model_complexity(0,1(default),2)',
                            type=int,
                            default=1)
        parser.add_argument("--min_detection_confidence",
                            help='min_detection_confidence',
                            type=float,
                            default=0.5)
        parser.add_argument("--min_tracking_confidence",
                            help='min_tracking_confidence',
                            type=float,
                            default=0.5)
        parser.add_argument('--enable_segmentation', action='store_true')
        parser.add_argument("--segmentation_score_th",
                            help='segmentation_score_threshold',
                            type=float,
                            default=0.5)

        parser.add_argument('--use_brect', action='store_true')
        parser.add_argument('--plot_world_landmark', action='store_true')

        args = parser.parse_args()

        return args


    def main(self):
        # 引数解析 #################################################################
        args = self.get_args()

        cap_device = args.device
        cap_width = args.width
        cap_height = args.height

        # upper_body_only = args.upper_body_only
        model_complexity = args.model_complexity
        min_detection_confidence = args.min_detection_confidence
        min_tracking_confidence = args.min_tracking_confidence
        self.enable_segmentation = args.enable_segmentation
        self.segmentation_score_th = args.segmentation_score_th

        self.use_brect = args.use_brect
        self.plot_world_landmark = args.plot_world_landmark

        # カメラ準備 ###############################################################
        self.cap = cv.VideoCapture(cap_device)
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)

        # モデルロード #############################################################
        mp_pose = mp.solutions.pose
        self.pose = mp_pose.Pose(
            # upper_body_only=upper_body_only,
            model_complexity=model_complexity,
            #enable_segmentation=enable_segmentation,   ###
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

        # FPS計測モジュール ########################################################
        self.cvFpsCalc = CvFpsCalc(buffer_len=10)

        # World座標プロット ########################################################
        if self.plot_world_landmark:
            
            fig = plt.figure()
            self.ax = fig.add_subplot(111, projection="3d")
            fig.subplots_adjust(left=0.0, right=1, bottom=0, top=1)

    def update(self):
        self.display_fps = self.cvFpsCalc.get()

        # カメラキャプチャ #####################################################
        ret, image = self.cap.read()
        
        image = image[self.y_start:self.y_end, self.x_start:self.x_end]

        image = cv.flip(image, 1)  # ミラー表示
        debug_image = copy.deepcopy(image)

        # 検出実施 #############################################################
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        results = self.pose.process(image)

        # 描画 ################################################################
        if self.enable_segmentation and results.segmentation_mask is not None:
            # セグメンテーション
            mask = np.stack((results.segmentation_mask, ) * 3,
                            axis=-1) > self.segmentation_score_th
            bg_resize_image = np.zeros(image.shape, dtype=np.uint8)
            bg_resize_image[:] = (0, 255, 0)
            debug_image = np.where(mask, debug_image, bg_resize_image)
        if results.pose_landmarks is not None:
            # 外接矩形の計算
            brect = self.calc_bounding_rect(debug_image, results.pose_landmarks)
            # 描画
            debug_image = self.draw_landmarks(
                debug_image,
                results.pose_landmarks,
                # upper_body_only,
            )
            debug_image = self.draw_bounding_rect(self.use_brect, debug_image, brect)

        # World座標プロット ###################################################
        if self.plot_world_landmark:
            if results.pose_world_landmarks is not None:
                self.plot_world_landmarks(
                    plt,
                    self.ax,
                    results.pose_world_landmarks,
                )

        # FPS表示
        if self.enable_segmentation and results.segmentation_mask is not None:
            fps_color = (255, 255, 255)
        else:
            fps_color = (0, 255, 0)
        cv.putText(debug_image, "FPS:" + str(self.display_fps), (10, 30),
                cv.FONT_HERSHEY_SIMPLEX, 1.0, fps_color, 2, cv.LINE_AA)

        # キー処理(ESC：終了) #################################################
        # key = cv.waitKey(1)
        # if key == 27:  # ESC
        #     break
        
        # 動画保存 ############################################################
        

        # 画面反映 #############################################################
        # cv.imshow('MediaPipe Pose Demo', debug_image)
        if self.on:
            if self.line:
                debug_image = cv.resize(debug_image, (960, 540))
                self.photo_line = ImageTk.PhotoImage(image=Image.fromarray(cv.cvtColor(debug_image, cv.COLOR_BGR2RGB)))
                self.canvas.delete("all")
                self.canvas.create_image(483, 273, image=self.photo_line)
            else:
                image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
                image = cv.resize(image, (960, 540))
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv.cvtColor(image, cv.COLOR_BGR2RGB)))
                self.canvas.delete("all")
                self.canvas.create_image(483, 273, image=self.photo)
        # アプリケーションの更新 #################################################

        self.after(1, self.update)
        
        # self.cap.release()
        # cv.destroyAllWindows()


    def calc_bounding_rect(self, image, landmarks):
        image_width, image_height = image.shape[1], image.shape[0]

        landmark_array = np.empty((0, 2), int)

        for _, landmark in enumerate(landmarks.landmark):
            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)

            landmark_point = [np.array((landmark_x, landmark_y))]

            landmark_array = np.append(landmark_array, landmark_point, axis=0)

        x, y, w, h = cv.boundingRect(landmark_array)

        return [x, y, x + w, y + h]


    def draw_landmarks(
        self,
        image,
        landmarks,
        # upper_body_only,
        visibility_th=0.5,
    ):
        image_width, image_height = image.shape[1], image.shape[0]
        radius = 3
        thick = 1

        landmark_point = []
        
        for index, landmark in enumerate(landmarks.landmark):
            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)
            landmark_z = landmark.z
            landmark_point.append([landmark.visibility, (landmark_x, landmark_y)])

            if landmark.visibility < visibility_th:
                continue
            
            prev = self.label_position["text"]
            if index == 0:  # 鼻
                #cv.circle(image, (landmark_x, landmark_y), radius, (0, 255, 0), thick)
                self.label_position["text"] = " 鼻:" + " x:" + str(landmark_x) + "y:" + str(landmark_y)
            if index == 1:  # 右目：目頭
                #cv.circle(image, (landmark_x, landmark_y), radius, (0, 255, 0), thick)
                self.label_position["text"] += " 右目：目頭:" + " x:" + str(landmark_x) + "y:" + str(landmark_y)
            if index == 2:  # 右目：瞳
                #cv.circle(image, (landmark_x, landmark_y), radius, (0, 255, 0), thick)
                self.label_position["text"] += " 右目：瞳:" + " x:" + str(landmark_x) + "y:" + str(landmark_y)
            if index == 3:  # 右目：目尻
                #cv.circle(image, (landmark_x, landmark_y), radius, (0, 255, 0), thick)
                self.label_position["text"] += " 右目：目尻:" + " x:" + str(landmark_x) + "y:" + str(landmark_y)
            if index == 4:  # 左目：目頭
                #cv.circle(image, (landmark_x, landmark_y), radius, (0, 255, 0), thick)
                self.label_position["text"] += " 左目：目頭:" + " x:" + str(landmark_x) + "y:" + str(landmark_y)
            if index == 5:  # 左目：瞳
                #cv.circle(image, (landmark_x, landmark_y), radius, (0, 255, 0), thick)
                self.label_position["text"] += " 左目：瞳:" + " x:" + str(landmark_x) + "y:" + str(landmark_y)
            if index == 6:  # 左目：目尻
                #cv.circle(image, (landmark_x, landmark_y), radius, (0, 255, 0), thick)
                self.label_position["text"] += " 左目：目尻:" + " x:" + str(landmark_x) + "y:" + str(landmark_y)
            if index == 7:  # 右耳
                #cv.circle(image, (landmark_x, landmark_y), radius, (0, 255, 0), thick)
                self.label_position["text"] += " 右耳:" + " x:" + str(landmark_x) + "y:" + str(landmark_y)
            if index == 8:  # 左耳
                #cv.circle(image, (landmark_x, landmark_y), radius, (0, 255, 0), thick)
                self.label_position["text"] += " 左耳:" + " x:" + str(landmark_x) + "y:" + str(landmark_y) + "\n"
            if index == 9:  # 口：右端
                #cv.circle(image, (landmark_x, landmark_y), radius, (0, 255, 0), thick)
                self.label_position["text"] += "  口：右端:" + " x:" + str(landmark_x) + "y:" + str(landmark_y)
            if index == 10:  # 口：左端
                #cv.circle(image, (landmark_x, landmark_y), radius, (0, 255, 0), thick)
                self.label_position["text"] += " 口：左端:" + " x:" + str(landmark_x) + "y:" + str(landmark_y)
            if index == 11:  # 右肩
                cv.circle(image, (landmark_x, landmark_y), radius, (0, 255, 0), thick)
                self.label_position["text"] += " 右肩:" + " x:" + str(landmark_x) + "y:" + str(landmark_y)
            if index == 12:  # 左肩
                cv.circle(image, (landmark_x, landmark_y), radius, (0, 255, 0), thick)
                self.label_position["text"] += " 左肩:" + " x:" + str(landmark_x) + "y:" + str(landmark_y)
            if index == 13:  # 右肘
                cv.circle(image, (landmark_x, landmark_y), radius, (0, 255, 0), thick)
                self.label_position["text"] += " 右肘:" + " x:" + str(landmark_x) + "y:" + str(landmark_y)
            if index == 14:  # 左肘
                cv.circle(image, (landmark_x, landmark_y), radius, (0, 255, 0), thick)
                self.label_position["text"] += " 左肘:" + " x:" + str(landmark_x) + "y:" + str(landmark_y)
            if index == 15:  # 右手首
                cv.circle(image, (landmark_x, landmark_y), radius, (0, 255, 0), thick)
                self.label_position["text"] += " 右手首:" + " x:" + str(landmark_x) + "y:" + str(landmark_y)
            if index == 16:  # 左手首
                cv.circle(image, (landmark_x, landmark_y), radius, (0, 255, 0), thick)
                self.label_position["text"] += " 左手首:" + " x:" + str(landmark_x) + "y:" + str(landmark_y) + "\n"
            if index == 17:  # 右手1(外側端)
                cv.circle(image, (landmark_x, landmark_y), radius, (0, 255, 0), thick)
                self.label_position["text"] += " 右手1(外側端):" + " x:" + str(landmark_x) + "y:" + str(landmark_y)
            if index == 18:  # 左手1(外側端)
                cv.circle(image, (landmark_x, landmark_y), radius, (0, 255, 0), thick)
                self.label_position["text"] += " 左手1(外側端):" + " x:" + str(landmark_x) + "y:" + str(landmark_y)
            if index == 19:  # 右手2(先端)
                cv.circle(image, (landmark_x, landmark_y), radius, (0, 255, 0), thick)
                self.label_position["text"] += " 右手2(先端):" + " x:" + str(landmark_x) + "y:" + str(landmark_y)
            if index == 20:  # 左手2(先端)
                cv.circle(image, (landmark_x, landmark_y), radius, (0, 255, 0), thick)
                self.label_position["text"] += " 左手2(先端):" + " x:" + str(landmark_x) + "y:" + str(landmark_y)
            if index == 21:  # 右手3(内側端)
                cv.circle(image, (landmark_x, landmark_y), radius, (0, 255, 0), thick)
                self.label_position["text"] += " 右手3(内側端):" + " x:" + str(landmark_x) + "y:" + str(landmark_y)
            if index == 22:  # 左手3(内側端)
                cv.circle(image, (landmark_x, landmark_y), radius, (0, 255, 0), thick)
                self.label_position["text"] += " 左手3(内側端):" + " x:" + str(landmark_x) + "y:" + str(landmark_y)
            if index == 23:  # 腰(右側)
                cv.circle(image, (landmark_x, landmark_y), radius, (0, 255, 0), thick)
                self.label_position["text"] += " 腰(右側):" + " x:" + str(landmark_x) + "y:" + str(landmark_y)
            if index == 24:  # 腰(左側)
                cv.circle(image, (landmark_x, landmark_y), radius, (0, 255, 0), thick)
                self.label_position["text"] += " 腰(左側):" + " x:" + str(landmark_x) + "y:" + str(landmark_y) + "\n"
            if index == 25:  # 右ひざ
                cv.circle(image, (landmark_x, landmark_y), radius, (0, 255, 0), thick)
                self.label_position["text"] += " 右ひざ:" + " x:" + str(landmark_x) + "y:" + str(landmark_y)
            if index == 26:  # 左ひざ
                cv.circle(image, (landmark_x, landmark_y), radius, (0, 255, 0), thick)
                self.label_position["text"] += " 左ひざ:" + " x:" + str(landmark_x) + "y:" + str(landmark_y)
            if index == 27:  # 右足首
                cv.circle(image, (landmark_x, landmark_y), radius, (0, 255, 0), thick)
                self.label_position["text"] += " 右足首:" + " x:" + str(landmark_x) + "y:" + str(landmark_y)
            if index == 28:  # 左足首
                cv.circle(image, (landmark_x, landmark_y), radius, (0, 255, 0), thick)
                self.label_position["text"] += " 左足首:" + " x:" + str(landmark_x) + "y:" + str(landmark_y)
            if index == 29:  # 右かかと
                cv.circle(image, (landmark_x, landmark_y), radius, (0, 255, 0), thick)
                self.label_position["text"] += " 右かかと:" + " x:" + str(landmark_x) + "y:" + str(landmark_y)
            if index == 30:  # 左かかと
                cv.circle(image, (landmark_x, landmark_y), radius, (0, 255, 0), thick)
                self.label_position["text"] += " 左かかと:" + " x:" + str(landmark_x) + "y:" + str(landmark_y)
            if index == 31:  # 右つま先}"
                cv.circle(image, (landmark_x, landmark_y), radius, (0, 255, 0), thick)
                self.label_position["text"] += " 右つま先:" + " x:" + str(landmark_x) + "y:" + str(landmark_y)
            if index == 32:  # 左つま先
                cv.circle(image, (landmark_x, landmark_y), radius, (0, 255, 0), thick)
                self.label_position["text"] += " 左つま先:" + " x:" + str(landmark_x) + "y:" + str(landmark_y)
                
            if not self.on:
                self.label_position["text"] = prev

            # if not upper_body_only:
            if False:
                cv.putText(image, "z:" + str(round(landmark_z, 3)),
                        (landmark_x - 10, landmark_y - 10),
                        cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1,
                        cv.LINE_AA)

        if len(landmark_point) > 0:
            # 右目
            #if landmark_point[1][0] > visibility_th and landmark_point[2][
            #        0] > visibility_th:
                #cv.line(image, landmark_point[1][1], landmark_point[2][1],
                #        (0, 255, 0), thick)
            #if landmark_point[2][0] > visibility_th and landmark_point[3][
            #        0] > visibility_th:
                #cv.line(image, landmark_point[2][1], landmark_point[3][1],
                #        (0, 255, 0), thick)

            # 左目
            #if landmark_point[4][0] > visibility_th and landmark_point[5][
            #        0] > visibility_th:
                #cv.line(image, landmark_point[4][1], landmark_point[5][1],
                #        (0, 255, 0), thick)
            #if landmark_point[5][0] > visibility_th and landmark_point[6][
            #        0] > visibility_th:
                #cv.line(image, landmark_point[5][1], landmark_point[6][1],
                #        (0, 255, 0), thick)

            # 口
            #if landmark_point[9][0] > visibility_th and landmark_point[10][
            #        0] > visibility_th:
                #cv.line(image, landmark_point[9][1], landmark_point[10][1],
                #        (0, 255, 0), thick)

            # 肩
            if landmark_point[11][0] > visibility_th and landmark_point[12][
                    0] > visibility_th:
                cv.line(image, landmark_point[11][1], landmark_point[12][1],
                        (0, 255, 0), thick)

            # 右腕
            if landmark_point[11][0] > visibility_th and landmark_point[13][
                    0] > visibility_th:
                cv.line(image, landmark_point[11][1], landmark_point[13][1],
                        (0, 255, 0), thick)
            if landmark_point[13][0] > visibility_th and landmark_point[15][
                    0] > visibility_th:
                cv.line(image, landmark_point[13][1], landmark_point[15][1],
                        (0, 255, 0), thick)

            # 左腕
            if landmark_point[12][0] > visibility_th and landmark_point[14][
                    0] > visibility_th:
                cv.line(image, landmark_point[12][1], landmark_point[14][1],
                        (0, 255, 0), thick)
            if landmark_point[14][0] > visibility_th and landmark_point[16][
                    0] > visibility_th:
                cv.line(image, landmark_point[14][1], landmark_point[16][1],
                        (0, 255, 0), thick)

            # 右手
            #if landmark_point[15][0] > visibility_th and landmark_point[17][
            #        0] > visibility_th:
                #cv.line(image, landmark_point[15][1], landmark_point[17][1],
                #        (0, 255, 0), thick)
            #if landmark_point[17][0] > visibility_th and landmark_point[19][
            #        0] > visibility_th:
                #cv.line(image, landmark_point[17][1], landmark_point[19][1],
                #        (0, 255, 0), thick)
            #if landmark_point[19][0] > visibility_th and landmark_point[21][
            #        0] > visibility_th:
                #cv.line(image, landmark_point[19][1], landmark_point[21][1],
                #        (0, 255, 0), thick)
            #if landmark_point[21][0] > visibility_th and landmark_point[15][
            #        0] > visibility_th:
                #cv.line(image, landmark_point[21][1], landmark_point[15][1],
                #        (0, 255, 0), thick)

            # 左手
            #if landmark_point[16][0] > visibility_th and landmark_point[18][
            #        0] > visibility_th:
                #cv.line(image, landmark_point[16][1], landmark_point[18][1],
                #        (0, 255, 0), thick)
            #if landmark_point[18][0] > visibility_th and landmark_point[20][
            #        0] > visibility_th:
                #cv.line(image, landmark_point[18][1], landmark_point[20][1],
                #        (0, 255, 0), thick)
            #if landmark_point[20][0] > visibility_th and landmark_point[22][
            #        0] > visibility_th:
                #cv.line(image, landmark_point[20][1], landmark_point[22][1],
                #        (0, 255, 0), thick)
            #if landmark_point[22][0] > visibility_th and landmark_point[16][
            #        0] > visibility_th:
                #cv.line(image, landmark_point[22][1], landmark_point[16][1],
                #        (0, 255, 0), thick)

            # 胴体
            if landmark_point[11][0] > visibility_th and landmark_point[23][
                    0] > visibility_th:
                cv.line(image, landmark_point[11][1], landmark_point[23][1],
                        (0, 255, 0), thick)
            if landmark_point[12][0] > visibility_th and landmark_point[24][
                    0] > visibility_th:
                cv.line(image, landmark_point[12][1], landmark_point[24][1],
                        (0, 255, 0), thick)
            if landmark_point[23][0] > visibility_th and landmark_point[24][
                    0] > visibility_th:
                cv.line(image, landmark_point[23][1], landmark_point[24][1],
                        (0, 255, 0), thick)

            if len(landmark_point) > 25:
                # 右足
                if landmark_point[23][0] > visibility_th and landmark_point[25][
                        0] > visibility_th:
                    cv.line(image, landmark_point[23][1], landmark_point[25][1],
                            (0, 255, 0), thick)
                if landmark_point[25][0] > visibility_th and landmark_point[27][
                        0] > visibility_th:
                    cv.line(image, landmark_point[25][1], landmark_point[27][1],
                            (0, 255, 0), thick)
                if landmark_point[27][0] > visibility_th and landmark_point[29][
                        0] > visibility_th:
                    cv.line(image, landmark_point[27][1], landmark_point[29][1],
                            (0, 255, 0), thick)
                if landmark_point[29][0] > visibility_th and landmark_point[31][
                        0] > visibility_th:
                    cv.line(image, landmark_point[29][1], landmark_point[31][1],
                            (0, 255, 0), thick)

                # 左足
                if landmark_point[24][0] > visibility_th and landmark_point[26][
                        0] > visibility_th:
                    cv.line(image, landmark_point[24][1], landmark_point[26][1],
                            (0, 255, 0), thick)
                if landmark_point[26][0] > visibility_th and landmark_point[28][
                        0] > visibility_th:
                    cv.line(image, landmark_point[26][1], landmark_point[28][1],
                            (0, 255, 0), thick)
                if landmark_point[28][0] > visibility_th and landmark_point[30][
                        0] > visibility_th:
                    cv.line(image, landmark_point[28][1], landmark_point[30][1],
                            (0, 255, 0), thick)
                if landmark_point[30][0] > visibility_th and landmark_point[32][
                        0] > visibility_th:
                    cv.line(image, landmark_point[30][1], landmark_point[32][1],
                            (0, 255, 0), thick)
                    
        return image


    def plot_world_landmarks(
        self,
        plt,
        ax,
        landmarks,
        visibility_th=0.5,
    ):
        landmark_point = []

        for index, landmark in enumerate(landmarks.landmark):
            landmark_point.append(
                [landmark.visibility, (landmark.x, landmark.y, landmark.z)])

        face_index_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        right_arm_index_list = [11, 13, 15, 17, 19, 21]
        left_arm_index_list = [12, 14, 16, 18, 20, 22]
        right_body_side_index_list = [11, 23, 25, 27, 29, 31]
        left_body_side_index_list = [12, 24, 26, 28, 30, 32]
        shoulder_index_list = [11, 12]
        waist_index_list = [23, 24]

        # 顔
        face_x, face_y, face_z = [], [], []
        for index in face_index_list:
            point = landmark_point[index][1]
            face_x.append(point[0])
            face_y.append(point[2])
            face_z.append(point[1] * (-1))

        # 右腕
        right_arm_x, right_arm_y, right_arm_z = [], [], []
        for index in right_arm_index_list:
            point = landmark_point[index][1]
            right_arm_x.append(point[0])
            right_arm_y.append(point[2])
            right_arm_z.append(point[1] * (-1))

        # 左腕
        left_arm_x, left_arm_y, left_arm_z = [], [], []
        for index in left_arm_index_list:
            point = landmark_point[index][1]
            left_arm_x.append(point[0])
            left_arm_y.append(point[2])
            left_arm_z.append(point[1] * (-1))

        # 右半身
        right_body_side_x, right_body_side_y, right_body_side_z = [], [], []
        for index in right_body_side_index_list:
            point = landmark_point[index][1]
            right_body_side_x.append(point[0])
            right_body_side_y.append(point[2])
            right_body_side_z.append(point[1] * (-1))

        # 左半身
        left_body_side_x, left_body_side_y, left_body_side_z = [], [], []
        for index in left_body_side_index_list:
            point = landmark_point[index][1]
            left_body_side_x.append(point[0])
            left_body_side_y.append(point[2])
            left_body_side_z.append(point[1] * (-1))

        # 肩
        shoulder_x, shoulder_y, shoulder_z = [], [], []
        for index in shoulder_index_list:
            point = landmark_point[index][1]
            shoulder_x.append(point[0])
            shoulder_y.append(point[2])
            shoulder_z.append(point[1] * (-1))

        # 腰
        waist_x, waist_y, waist_z = [], [], []
        for index in waist_index_list:
            point = landmark_point[index][1]
            waist_x.append(point[0])
            waist_y.append(point[2])
            waist_z.append(point[1] * (-1))
                
        ax.cla()
        ax.set_xlim3d(-1, 1)
        ax.set_ylim3d(-1, 1)
        ax.set_zlim3d(-1, 1)

        ax.scatter(face_x, face_y, face_z)
        ax.plot(right_arm_x, right_arm_y, right_arm_z)
        ax.plot(left_arm_x, left_arm_y, left_arm_z)
        ax.plot(right_body_side_x, right_body_side_y, right_body_side_z)
        ax.plot(left_body_side_x, left_body_side_y, left_body_side_z)
        ax.plot(shoulder_x, shoulder_y, shoulder_z)
        ax.plot(waist_x, waist_y, waist_z)
        
        plt.pause(.001)

        return


    def draw_bounding_rect(self, use_brect, image, brect):
        if use_brect:
            # 外接矩形
            cv.rectangle(image, (brect[0], brect[1]), (brect[2], brect[3]),
                        (0, 255, 0), 2)

        return image
    
    def t1(self):
        camera = cv.VideoCapture(self.choseCamNumber)                               
        
        # 動画ファイル保存用の設定
        fps = 10                   # カメラのFPSを取得
        print("fps", fps)
        w = int(camera.get(cv.CAP_PROP_FRAME_WIDTH))              # カメラの横幅を取得
        h = int(camera.get(cv.CAP_PROP_FRAME_HEIGHT))             # カメラの縦幅を取得
        fourcc = cv.VideoWriter_fourcc('m', 'p', '4', 'v')        # 動画保存時のfourcc設定（mp4用）
        dt_now = datetime.datetime.now()
        self.file_time = time.time()
        self.name = dt_now.strftime("%Y%m%d%H%M%S") + "{:06d}".format(dt_now.microsecond)
        date = self.name + ".mp4"
        video = cv.VideoWriter(date, fourcc, fps, (w, h))  # 動画の仕様（ファイル名、fourcc, FPS, サイズ）
        

        while True:
            start = time.time()
            ret, frame = camera.read()                             # フレームを取得

            video.write(frame)                                     # 動画を1フレームずつ保存する

            if not self.REC:
                print("ok")
                camera.release()
                video.release()
                break
            
            end = time.time()
            t = end - start
            if t < 1/fps:
                time.sleep(1/fps - t)
                
            
# class Application2(tk.Frame):
#     def __init__(self, root):
#         super().__init__(root)
#         self.root = root
#         self.pack()
#         self.root.geometry("1270x720")
#         self.root.title("test")
#         self.video = cv.VideoCapture("さかなー.mp4")
#         self.createWidgets()
#         self.play()
        
#     def createWidgets(self):
#         self.canvas_video = tk.Canvas(self.root, width=960, height=540)
#         self.canvas_video.pack()
        
#     def delWindow(self):
#         self.root.destroy()
        
#     def play(self):
#         ret, debug_image = self.video.read()
#         if not ret:
#             self.video.set(cv.CAP_PROP_POS_FRAMES, 0)
        
#         debug_image = cv.resize(debug_image, (960, 540))
#         self.photo_line = ImageTk.PhotoImage(image=Image.fromarray(cv.cvtColor(debug_image, cv.COLOR_BGR2RGB)))
#         self.canvas_video.delete("all")
#         self.canvas_video.create_image(483, 273, image=self.photo_line)
        
#         self.after(1, self.play)

if __name__ == '__main__':
    root = tk.Tk()
    root.title("姿勢推定")
    root.geometry("1270x720")
    
    app = Application(root)
    app.mainloop()
