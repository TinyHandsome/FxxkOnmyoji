#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Li Tian
@contact: litian_cup@163.com
@software: pycharm
@file: get_fullscreen.py
@time: 2021/1/10 上午8:21
@desc: 获取整个桌面的截图
        1. [python打印出所有窗体的句柄类名和标题和句柄（可显示子句柄）](https://www.cnblogs.com/myfriend/articles/12509278.html)
        2. [python3应用windows api对后台程序窗口及桌面截图并保存的方法](https://www.jb51.net/article/168576.htm)
        3. [如何利用Python和win32编程避免重复性体力劳动（一）——开始、FindWindow和FindWindowEx](https://blog.csdn.net/seele52/article/details/17504925)
        4. [通过截图匹配原图中的位置（opencv）](https://blog.csdn.net/ns2250225/article/details/60334176/)
           Aircv是一款基于Python-opencv2的目标定位。
        5.

"""
import win32gui, win32ui, win32con
from ctypes import windll
from PIL import Image
import cv2
import numpy as np
import copy


def find_onmyoji_handle():
    """找到所有阴阳师的界面的句柄，如果是多个同类的窗口，谁最后打开的，谁优先获取"""
    # 获取后台窗口的句柄，注意后台窗口不能最小化
    handle_name = '阴阳师-网易游戏'
    # 获取第一个阴阳师的句柄
    handle_last = win32gui.FindWindowEx(0, 0, "Win32Window", handle_name)
    handles = [handle_last]
    # 遍历获取其他阴阳师的句柄
    while True:
        handle_last = win32gui.FindWindowEx(0, handle_last, "Win32Window", handle_name)
        if handle_last == 0:
            break
        handles.append(handle_last)

    return handles


def show_handle(hWnd):
    """获取句柄的截图"""
    # 获取句柄窗口的大小信息
    left, top, right, bot = win32gui.GetWindowRect(hWnd)
    width = right - left
    height = bot - top
    # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    hWndDC = win32gui.GetWindowDC(hWnd)
    # 创建设备描述表
    mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    # 创建内存设备描述表
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建位图对象准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 为bitmap开辟存储空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    # 将截图保存到saveBitMap中
    saveDC.SelectObject(saveBitMap)
    # 保存bitmap到内存设备描述表
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)

    def save_by_PIL(is_save=False, is_show=False):
        """方法1"""
        # 获取位图信息
        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)
        # 生成图像
        im_PIL = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)

        if is_save:
            im_PIL.save("im_PIL.png")
        if is_show:
            im_PIL.show()
        return im_PIL

    def save_by_windows_api(is_save=False):
        """方法2"""
        if is_save:
            saveBitMap.SaveBitmapFile(saveDC, "img_Winapi.bmp")
        return saveBitMap

    def save_by_opencv(is_save=False, is_show=False):
        """方法3"""
        # 获取位图信息
        signedIntsArray = saveBitMap.GetBitmapBits(True)
        # PrintWindow成功，保存到文件，显示到屏幕
        im_opencv = np.frombuffer(signedIntsArray, dtype='uint8')
        im_opencv.shape = (height, width, 4)
        cv2.cvtColor(im_opencv, cv2.COLOR_BGRA2RGB)

        save_path = "roaming/im_opencv.jpg"
        if is_save:
            cv2.imwrite(save_path, im_opencv, [int(cv2.IMWRITE_JPEG_QUALITY), 100])  # 保存
        if is_show:
            cv2.namedWindow('阴阳师后台截图')  # 命名窗口
            cv2.imshow("阴阳师后台截图", im_opencv)  # 显示
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        return save_path

    return save_by_opencv(is_save=True)


def locate_pic(im_source_path, im_search_path):
    """获取对应图片在 im_source 的位置"""
    im_search = cv2.imread(im_search_path)
    im_source = cv2.imread(im_source_path)
    im_search_width = im_search.shape[0]
    im_search_height = im_search.shape[1]
    cv2.imshow('Image', im_search)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.imshow('Image', im_source)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    exit()

    res = cv2.matchTemplate(im_source, im_search, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    print(min_val, max_val, min_loc, max_loc)
    img = cv2.rectangle(im_source, max_loc, (max_loc[0] + im_search_height, max_loc[1] + im_search_width), (0, 0, 255), 2)
    cv2.imshow('Image', img)
    print(max_loc[0] + im_search_width, max_loc[1] + im_search_height)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    for handle in find_onmyoji_handle():
        im_opencv = show_handle(handle)
        aim_img = r'imgs\御魂\挑战.png'
        locate_pic(im_opencv, aim_img)
