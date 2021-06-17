# coding:utf-8
# /usr/bin/python3
"""
动态检测相机图像中的aruco标记
"""
import numpy as np
import time
import cv2
import cv2.aruco as aruco

# 标定得到的畸变系数
dist = np.array(([[−0.32185929, 0.10731995, −0.00102685, 0.00097965, −0.01617569]]))
mtx = np.array([[270.08621165,   0.,         340.20538897],
 [  0.,         269.19788136, 228.54706624],
 [  0.,           0.,           1.        ]])
# 矫正后的相机参数
new_mtx = np.array([[269.66421509,   0.,         339.67384683],
 [  0.,         268.63705444, 228.07093163],
 [  0.,           0.,           1.        ]])
roi = (27, 21, 583, 429)

cap = cv2.VideoCapture(0)
if cap.isOpened():
    print("Succeed to turn on the camera.")
else:
    print("Fail to turn on the camera!")
    print("Program exits now.")
    exit()

font = cv2.FONT_HERSHEY_SIMPLEX # font for displaying text (below)

#num = 0
while True:
    ret, frame = cap.read()
    h1, w1 = frame.shape[:2]    # 原始尺寸

    # 纠正畸变
    new_mtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (h1, w1), 0, (h1, w1))  # 这一步可以不要
    dst1 = cv2.undistort(frame, mtx, dist, None, new_mtx)
    x, y, w2, h2 = roi  # 剪裁尺寸
    dst1 = dst1[y:y+h2, x:x+w2]
    frame = dst1


    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_250)
    parameters =  aruco.DetectorParameters_create()
    dst1 = cv2.undistort(frame, mtx, dist, None, new_mtx)

    # 检测标志。返回标志（可能有多个）的ID和4个角点的坐标（二维）
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    if ids is not None:
        # 姿态估计。标志边长为0.08m
        rvec, tvec, obj_points = aruco.estimatePoseSingleMarkers(corners, 0.08, mtx, dist)
        print("rvec, tvec", rvec, tvec)

        for i in range(rvec.shape[0]):
            aruco.drawAxis(frame, mtx, dist, rvec[i,:,:], tvec[i,:,:], 0.03)
            aruco.drawDetectedMarkers(frame, corners)
            # aruco.drawDetectedMarkers(frame, corners, ids[i])
            cv2.putText(frame, "Id:"+str(ids), (0,64), font, 1, (0,255,0), 2, cv2.LINE_AA)
    else:
        cv2.putText(frame, "No Ids", (0,64), font, 1, (0,255,0), 2, cv2.LINE_AA)


    # 显示结果框架
    cv2.imshow("frame",frame)

    key = cv2.waitKey(1)

    if key == 27:         # 按esc键退出
        print('esc break...')
        cap.release()
        cv2.destroyAllWindows()
        break

    if key == ord(' '):   # 按空格键保存
#        num = num + 1
#        filename = "frames_%s.jpg" % num  # 保存一张图像
        filename = str(time.time())[:10] + ".jpg"
        cv2.imwrite(filename, frame)
