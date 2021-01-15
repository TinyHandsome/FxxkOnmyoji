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
from random import uniform


class TipTime:
    def __init__(self):
        self.click_many_times_range = (0.2, 0.5)

    def tip(self):
        temp = uniform(self.click_many_times_range[0], self.click_many_times_range[1])
        time.sleep(temp)
