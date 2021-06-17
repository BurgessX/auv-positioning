# coding=utf-8
# /usr/bin/python3
"""
相机标定
"""
import cv2
import numpy as np
import glob

## 1.找棋盘角点
print("1.找棋盘角点")
# 设置寻找亚像素角点的参数，采用的停止准则是最大循环次数30和最大误差容限0.001
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001) # 阈值
# 棋盘角点数
w = 9   # 宽度方向 10 - 1
h = 6   # 高度方向 7  - 1
# 世界坐标系中的棋盘角点的索引,例如(0,0,0), (1,0,0), (2,0,0) ....,(8,5,0)，去掉Z坐标，记为二维矩阵
objp = np.zeros((w*h,3), np.float32)
objp[:,:2] = np.mgrid[0:w,0:h].T.reshape(-1,2) # mgrid是生成角点的索引，T是转置，reshape转成n行2列
objp = objp * 20.0  # 20.0mm是每个格子的边长，所以最终objp是实际图像各角点的坐标

# 初始化储存棋盘角点坐标的列表
objpoints = [] # 在世界坐标系中的三维点
imgpoints = [] # 在图像平面的二维点
# 加载所有棋盘图片
images = glob.glob('./chess_pictures2/*.jpg')

i = 0
for fname in images:
    img = cv2.imread(fname)
    h1, w1 = img.shape[:2] # 获取图像的高和宽(720,1280)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # 图像灰度化
    ret, corners = cv2.findChessboardCorners(gray, (w,h), None) # 寻找棋盘角点
    # 如果找到足够点对，将其存储起来
    if ret == True:
        print("i:", i)
        i = i+1
        # 在原角点的基础上寻找亚像素角点
        cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria) # 最大搜索范围为窗口边长的一半，即11*2+1=23；最小范围不指定
        # 保存角点数据
        objpoints.append(objp)
        imgpoints.append(corners)
        # 将角点在图像上显示
        cv2.drawChessboardCorners(img, (w,h), corners, ret)
        cv2.namedWindow('findCorners', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('findCorners', 640, 480)
        cv2.imshow('findCorners', img)
        cv2.waitKey(200)

cv2.destroyAllWindows()



## 2.标定
print("2.标定")
ret, mtx, dist, rvecs, tvecs = \
    cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
# ret - RMS重投影误差
# mtx - 相机矩阵/内参矩阵（3X3）
# dist - 畸变系数(k_1,k_2,p_1,p_2,k_3)
# rvecs - 旋转向量
# tvecs - 平移向量
print("ret:", ret)
print("相机矩阵（内参）:\n", mtx)
print("畸变系数:\n", dist)
print("旋转向量（外参）:\n", rvecs)
print("平移向量（外参）:\n", tvecs)


## 3.矫正
print("3.矫正")
ori_img = cv2.imread("./chess_pictures2/img10.jpg") # 待矫正的原始图片
cv2.imshow('ori_img', ori_img)
cv2.waitKey(0)
h1, w1 = ori_img.shape[:2] # 获取原图像的高和宽(720,1280)

new_mtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w1,h1), 1.0, (w1,h1)) # 通过畸变参数矫正相机矩阵（内参），得到新的相机内参。

# 这里比例系数alpha=0，表示最小化不想要的像素（黑色部分），这样裁剪掉的部分就比较少
x, y, w2, h2 = roi # region of interest：0,0,<1280,<720，后面根据此尺寸裁剪
print("矫正后新的相机矩阵（内参）:\n", new_mtx)

# 方法一
dst1 = cv2.undistort(ori_img, mtx, dist, None, new_mtx)
if dst1 is None:
    print("dst1 is None")
    exit(-1)
else:
    cv2.imshow('dst1', dst1)
    cv2.waitKey(0)

# 方法二
mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, new_mtx, (w1,h1), 5)
dst2 = cv2.remap(ori_img, mapx, mapy, cv2.INTER_LINEAR)
if dst2 is None:
    print("dst2 is None")
    exit(-1)
else:
    cv2.imshow('dst2', dst2)
    cv2.waitKey(0)

## 4.裁剪感兴趣的部分并保存
print("4.裁剪感兴趣的部分并保存")
dst1 = dst1[y:y+h2, x:x+w2]
dst2 = dst2[y:y+h2, x:x+w2]
cv2.imwrite("./calibrated_pictures/dst1.png", dst1)
cv2.imwrite("./calibrated_pictures/dst2.png", dst2)

cv2.destroyAllWindows()
