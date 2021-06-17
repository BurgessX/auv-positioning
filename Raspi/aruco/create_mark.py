#-*- coding: UTF-8 -*-
#!/usr/bin/python3
"""
生成aruco标记图
"""
import cv2
import numpy as np
import os

# 加载预定义的字典
dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_250)

# 生成用于打印的标记
markerImage = np.zeros((200, 200), dtype=np.uint8)
markerImage = cv2.aruco.drawMarker(dictionary, 11, 200, markerImage, 1)

if not os.path.exists('marks'):
    os.mkdir('marks')

cv2.imwrite("./marks/marker11.png", markerImage)
