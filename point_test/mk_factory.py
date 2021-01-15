#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Li Tian
@contact: litian_cup@163.com
@software: pycharm
@file: mk_factory.py
@time: 2020/8/31 17:25
@desc: 鼠标键盘模拟工场
"""
from point_test.mouse_action import MouseAction
from point_test.keyboard_action import KeyboardAction
from point_test.tip_time import TipTime


class MKFactory:
    def __init__(self):
        self.m = MouseAction()
        self.k = KeyboardAction()
        self.t = TipTime()
        self.state = True
        self.escape_steps = [1, 2, 3]

    def colorCheck(self, info, coordinate):
        """
        检查颜色是否对应，整个操作流程是否进行的标志
        :param info: r,g,b
        :param coordinate: 坐标：(x, y)
        """
        # 进行循环的时候检测是否满足循环条件，即按键颜色是否符合目标颜色
        rgb_list = [int(a) for a in info.split(',')]
        self.state = self.m.check_mouse_color(rgb_list, coordinate)

        return self.state

    def l1(self, xy):
        """单击，停顿"""
        self.m.mouse_click(xy[0], xy[1])
        self.t.tip()

    def l2(self, xy):
        """双击，停顿"""
        self.m.mouse_doubleclick(xy[0], xy[1])
        self.t.tip()

    def r1(self, xy):
        """右键单击，停顿"""
        self.m.mouse_right_click(xy[0], xy[1])
        self.t.tip()

    def r2(self, xy):
        """右键双击，停顿"""
        self.m.mouse_right_doubleclick(xy[0], xy[1])
        self.t.tip()

    def k_str(self, strs):
        """输入str，停顿"""
        self.k.key_input(strs)
        self.t.tip()
