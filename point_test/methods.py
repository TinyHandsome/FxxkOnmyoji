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


def build_thread(func, func_name, args=()):
    """建立线程"""
    t = Thread(target=func, name='【线程】' + func_name, daemon=True, args=args)
    # 设置守护线程，主线程退出不必等待该线程
    # print(t.name + '，启动...')
    t.start()
