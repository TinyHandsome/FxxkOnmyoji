#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Li Tian
@contact: litian_cup@163.com
@software: pycharm
@file: methods.py
@time: 2021/1/18 17:42
@desc: 常用methods
"""
from threading import Thread
from dataclasses import dataclass

# def build_thread(func, func_name, args=()):
#     """建立线程"""
#     t = Thread(target=func, name='【线程】' + func_name, daemon=True, args=args)
#     # 设置守护线程，主线程退出不必等待该线程
#     # print(t.name + '，启动...')
#     t.start()


class MyThread(Thread):
    def __init__(self, func, func_name, args=()):
        super().__init__()
        self.func = func
        self.func_name = func_name
        self.args = args

    def __post_init__(self):
        # 实现暂停功能的flag
        self.stop_flag = False

    def build_thread(self):
        """建立线程"""
        # https://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread
        t = Thread(target=self.func, name='【线程】' + self.func_name, daemon=True, args=self.args)
        # 设置守护线程，主线程退出不必等待该线程
        # print(t.name + '，启动...')
        t.start()
