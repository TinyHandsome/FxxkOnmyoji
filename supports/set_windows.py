#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Li Tian
@contact: litian_cup@163.com
@software: pycharm
@file: set_windows.py
@time: 2021/1/17 下午12:40
@desc: 设置所有阴阳师的界面为目标的位置和大小
        1. [python打印出所有窗体的句柄类名和标题和句柄（可显示子句柄）](https://www.cnblogs.com/myfriend/articles/12509278.html)
        2. [python3应用windows api对后台程序窗口及桌面截图并保存的方法](https://www.jb51.net/article/168576.htm)
        3. [如何利用Python和win32编程避免重复性体力劳动（一）——开始、FindWindow和FindWindowEx](https://blog.csdn.net/seele52/article/details/17504925)
        4. [通过截图匹配原图中的位置（opencv）](https://blog.csdn.net/ns2250225/article/details/60334176/)
           Aircv是一款基于Python-opencv2的目标定位。
        5. [窗口的位置：GetWindowRect与MoveWindow等](https://blog.csdn.net/fyyyr/article/details/79252897?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-1.control&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-1.control)
        6. [python---win32gui、win32con、win32api：winAPI操作](https://www.cnblogs.com/liming19680104/p/11988565.html)
        7. [Python基础系列讲解-自动控制windows桌面](https://www.imooc.com/article/288884)
"""

from dataclasses import dataclass

import win32con
import win32gui
# import win32ui
from PIL import Image
import numpy as np


@dataclass
class SetWin:
    def __post_init__(self):
        ...

    def gbk2utf8(self, s):
        """gbk转utf8"""
        return str(s.encode('utf-8'), encoding='utf-8')
        # return s

    def show_window_attr(self, hwnd):
        """显示窗口的属性"""
        if not hwnd:
            return

        # 中文系统默认的title是gb2312的编码
        title = win32gui.GetWindowText(hwnd)
        title = self.gbk2utf8(title)
        class_name = win32gui.GetClassName(hwnd)

        print('窗口句柄：{0}'.format(hwnd))
        print('窗口标题：{0}'.format(title))
        print('窗口类名：{0}'.format(class_name))
        print('*' * 100)

    def show_windows(self, hwnd_list):
        """展示所有窗口列表"""
        for h in hwnd_list:
            self.show_window_attr(h)

    def show_tops_windows(self):
        """列出所有顶级窗口"""
        hwnd_list = []
        win32gui.EnumWindows(lambda hwnd, param: param.append(hwnd), hwnd_list)
        self.show_windows(hwnd_list)

        return hwnd_list

    def show_child_windows(self, parent):
        """列出所有子窗口"""
        if not parent:
            return

        hwnd_child_list = []
        win32gui.EnumChildWindows(parent, lambda hwnd, param: param.append(hwnd), hwnd_child_list)
        self.show_windows(hwnd_child_list)
        return hwnd_child_list

    def find_onmyoji_handle(self):
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

    def get_handle_rect(self, hWnd):
        """获取窗口的矩形位置"""
        # 获取句柄窗口的大小信息，这里我们主要用屏幕坐标系
        # GetWindowRect()获取的是以屏幕左上角为(0,0)点的窗口区域，是屏幕坐标系。
        left, top, right, bot = win32gui.GetWindowRect(hWnd)

        # GetClentRect()获取的是自身客户区，其左上角以自身客户区的左上角为(0,0)。
        # left, top, right, bot = win32gui.GetClientRect(hWnd)

        # print(left, top, right, bot)
        return left, top, right, bot

    def move_rect(self, hWnd, pos):
        """移动窗口到目标位置"""
        win32gui.MoveWindow(hWnd, pos[0], pos[1], pos[2], pos[3], 0)
        self.get_handle_rect(hWnd)

    def show_handle(self, hWnd, return_type='cv'):
        """获取句柄的截图，否贼返回图片"""
        left, top, right, bot = self.get_handle_rect(hWnd)
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
            return im_opencv

        if return_type == 'pil':
            return save_by_PIL(True, False)
        elif return_type == 'win':
            return save_by_windows_api(False)
        else:
            return save_by_opencv(is_save=False, is_show=True)


if __name__ == '__main__':
    sw = SetWin()
    handles = sw.find_onmyoji_handle()
    print(handles)
    locs = [(-7, 0, 500, 560), (-7, 556, 500, 560)]
    for h in range(len(handles)):
        # sw.get_handle_rect(handles[h])
        sw.move_rect(handles[h], locs[h])

    """查看所有顶级窗口"""
    # sw.show_tops_windows()
    """查看所有子窗口"""
    # sw.show_child_windows(199546)
