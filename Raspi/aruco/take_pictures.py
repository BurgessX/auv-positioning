# coding:utf-8
# /usr/bin/python3
"""
拍摄照片，用来生成若干张校正用的棋盘图的图片
"""
import cv2

# ID = 0
# while True:
#     camera=cv2.VideoCapture(ID)
#     if camera.isOpened():
#         print("Camera is opened.")
#         break
#     else:
#         ID += 1

camera = cv2.VideoCapture(0)
if not camera.isOpened():
    print("Camera is not opened.")
    exit(-1)

i = 0
while 1:
    (grabbed, img) = camera.read()
    cv2.imshow('img',img)   # 展示图片
    key = cv2.waitKey(1)
    if key & 0xFF == ord('j'):  # 按j保存一张图片
        i += 1
        u = str(i)
        firename=str('./chess_pictures2/img'+u+'.jpg')
        cv2.imwrite(firename, img)  # 保存图片
        print('写入：',firename)
    elif key & 0xFF == ord('q'):   # 按q退出
        break

cv2.destroyAllWindows()
# cv2.waitKey()是在一个给定的时间内(单位ms)等待用户按键触发；如果用户没有按下键,则继续等待 (循环)