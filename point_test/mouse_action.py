#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Li Tian
@contact: litian_cup@163.com
@software: pycharm
@file: mouse_action.py
@time: 2020/8/31 14:10
@desc: 处理鼠标
"""

from pymouse import *
import pyautogui
from dataclasses import dataclass


@dataclass
class Location:
    x: int
    y: int
    r: int
    g: int
    b: int

    def __post_init__(self):
        pass

    def get_info(self):
        return (self.x, self.y), (self.r, self.g, self.b)


class MouseAction:
    def __init__(self):
        self.m = PyMouse()

    def mouse_move_to(self, x, y):
        """鼠标移动到x，y"""
        self.m.move(x, y)

    def mouse_click(self, x, y):
        """将鼠标移动到(x,y)，左键点一次"""
        self.m.click(x, y, 1, 1)

    def mouse_right_click(self, x, y):
        """将鼠标移动到(x,y)，右键点一次"""
        self.m.click(x, y, 2, 1)

    def mouse_doubleclick(self, x, y):
        """将鼠标移动到(x,y)，左键点两次"""
        self.m.click(x, y, 1, 2)

    def mouse_right_doubleclick(self, x, y):
        """将鼠标移动到(x,y)，左键点两次"""
        self.m.click(x, y, 2, 2)

    def get_mouse_postion(self, is_print=False):
        """获取鼠标的位置，是否打印"""
        p = self.m.position()
        if is_print:
            print(p)
        return p[0], p[1]

    def get_mouse_color(self, is_print=False):
        """获取鼠标的颜色，是否打印"""
        p = self.m.position()
        try:
            c = pyautogui.screenshot().getpixel(p)
        except Exception as e:
            c = (-1, -1, -1)
        if is_print:
            print(c)
        return c

    def get_mouse_postion_color(self):
        """获取鼠标所在位置的坐标和颜色"""
        x, y = self.get_mouse_postion()
        r, g, b = self.get_mouse_color()
        return Location(x, y, r, g, b)

    def check_mouse_color(self, rgb, position=None) -> bool:
        """
        检查颜色是否符合，如果没有指定位置，则为当前鼠标位置的颜色是否对应目标颜色
        :return 是否匹配成功，True 或 False
        """
        if position is None:
            position = self.m.position()
        return pyautogui.pixelMatchesColor(position[0], position[1], rgb)


if __name__ == '__main__':
    mouse = MouseAction()
    mouse.get_mouse_postion(True)
    mouse.get_mouse_color(True)
    print(mouse.get_mouse_color())
