import numpy as np
import time
import cv2
import cv2.aruco as aruco
import socket

raspi_host = '192.168.7.1'
# raspi_host = '127.0.0.1'   # test
raspi_port = 10000

BBB_tx_host = '192.168.7.2'
# BBB_tx_host = '127.0.0.1'   # test
BBB_tx_port = 10001

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((raspi_host, raspi_port))
print("UDP server", (raspi_host, raspi_port), "is running.")

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
last = False    # 上次循环有没有数据
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

        # 发送位姿数据
        # print("rvec, tvec", rvec, tvec)
        if last == True:   # 上次循环也有数据，已经打印了Send，这次不打印
            pass
        else:
            print("Start sending messages to", (BBB_tx_host, BBB_tx_port), ".")
            last = True

        position_data = "rvec=" + str(rvec[0,0,:]) + "\ntvec=" + str(tvec[0,0,:])   # 这里只发送一个标志的位姿数据
        print("Sending data to", (BBB_tx_host, BBB_tx_port), ":")
        print(position_data)
        udp_socket.sendto(bytes(position_data,encoding="utf-8"), (BBB_tx_host, BBB_tx_port))  # send back

        for i in range(rvec.shape[0]):
            aruco.drawAxis(frame, mtx, dist, rvec[i,:,:], tvec[i,:,:], 0.03)
            aruco.drawDetectedMarkers(frame, corners)
            # aruco.drawDetectedMarkers(frame, corners, ids[i])
            cv2.putText(frame, "Id:"+str(ids), (0,64), font, 1, (0,255,0), 2, cv2.LINE_AA)

    else:
        cv2.putText(frame, "No Ids", (0,64), font, 1, (0,255,0), 2, cv2.LINE_AA)
        if last == False:   # 上次循环也没数据，已经打印了Stop，这次不打印
            pass
        else:
            print("Stop sending.")
            last = False


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
