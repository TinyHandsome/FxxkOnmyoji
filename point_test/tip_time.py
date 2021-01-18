#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Li Tian
@contact: litian_cup@163.com
@software: pycharm
@file: tip_time.py
@time: 2020/8/31 17:33
@desc: 暂停的时间类，暂停的时间是随机时间。
        【参考链接】
            1. [random函数的用法](https://www.runoob.com/python/func-number-random.html)
        【功能概述】
            1. 鼠标连续点击随机时间：[0.2, 0.5]，用途：结算界面疯狂点击的时候
"""
import time
from random import uniform, randrange
from configure_tools import Configure


class TipTime:
    def __init__(self):
        self.conf = Configure('configures/config.ini')
        # 鼠标狂点时间间隔
        self.click_many_times_range = (self.conf.get_option('time', 'click_many_times_min', 'float'),
                                       self.conf.get_option('time', 'click_many_times_max', 'float'))
        # 颜色检测时间间隔
        self.color_check_range = (self.conf.get_option('time', 'color_check_min', 'float'),
                                  self.conf.get_option('time', 'click_many_times_max', 'float'))
        # 鼠标点击偏移量（上下左右）
        self.mouse_bias = self.conf.get_option('mouse', 'mouse_bias', 'int')

    def tip(self, flag='mouse'):
        if flag == 'mouse':
            aim_set = self.click_many_times_range
        elif flag == 'color':
            aim_set = self.color_check_range
        else:
            raise Exception('狗贼，时间有问题！')

        temp = uniform(aim_set[0], aim_set[1])
        time.sleep(temp)

    def get_mouse_bias(self):
        """获取鼠标偏移量"""

        def gb():
            return randrange(-self.mouse_bias, self.mouse_bias)

        return gb(), gb()


if __name__ == '__main__':
    print(TipTime().get_mouse_bias())
