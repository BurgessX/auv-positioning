# coding:utf-8
# /usr/bin/python3
"""
检测图片中的aruco标记
"""
import numpy as np
import time
import cv2
import cv2.aruco as aruco

# 读取图片
frame=cv2.imread('./mark_pictures/IMG_20210518_160513.jpg')
# 调整图片大小
frame=cv2.resize(frame,None,fx=0.2,fy=0.2,interpolation=cv2.INTER_CUBIC)
# 灰度话
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# 设置预定义的字典
aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_250)
# 使用默认值初始化检测器参数
parameters =  aruco.DetectorParameters_create()
# 使用aruco.detectMarkers()函数可以检测到marker，返回ID和标志板的4个角点坐标
corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
# 画出标志位置
aruco.drawDetectedMarkers(frame, corners, ids)


cv2.imshow("frame", frame)
cv2.waitKey(0)  # 无限等待，按任意键继续
cv2.destroyAllWindows()
