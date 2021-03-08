#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Li Tian
@contact: litian_cup@163.com
@software: pycharm
@file: info_pip.py
@time: 2021/2/4 14:20
@desc: 信息管道
"""
from dataclasses import dataclass
import time
from tkinter import StringVar, Label
from _io import TextIOWrapper


@dataclass
class InfoPip:
    current_info: StringVar
    history_info: StringVar
    l_first: Label
    log_file: TextIOWrapper

    def __post_init__(self):
        # 左边是入口，右边是出口
        self.queue = [''] * 3
        self.first_color = ''

    def get_two_var(self):
        """将当前的pip结果放到var中去，获得两个str"""
        # 第一个label的颜色，第一个label的info，下一个label的info
        return self.first_color, self.queue[0], '\n'.join(self.queue[1:])

    def set_first_line(self, info, color):
        """进入新的值和颜色，全体数据往右移"""
        self.first_color = color
        for i in range(len(self.queue) - 1, 0, -1):
            self.queue[i] = self.queue[i - 1]
        self.queue[0] = info

    def get_pip_history(self, info, color):
        """将上述功能进行合并，进入新的信息，获取输出的信息"""
        self.set_first_line(info, color)
        return self.get_two_var()

    def show_info(self, word, fg='green'):
        """输出问题"""
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        w1_color, w1, w2 = self.get_pip_history(word, fg)

        self.current_info.set(w1)
        self.l_first.configure(fg=fg)

        self.history_info.set(w2)

        # 写入日志
        self.log_file.write(current_time + ': \n' + w1 + '\n\n')

    def info(self, word, type):
        """简化输出"""
        if type == 1:
            # 点击事件
            self.show_info('【选择】' + word + '...', 'black')
        elif type == 2:
            # 错误事件
            self.show_info('【错误】' + word + '...', 'red')
        elif type == 3:
            # 成功事件
            self.show_info('【成功】' + word + '...', 'green')