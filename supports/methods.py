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
        1. [线程的关闭](https://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread
)
"""
from threading import Thread
import threading
import time


def build_thread(func, func_name, args=()):
    """建立线程"""
    t = MyThread(target=func, name='【线程】' + func_name, daemon=True, args=args)
    # 设置守护线程，主线程退出不必等待该线程
    # print(t.name + '，启动...')
    t.start()



class Job(threading.Thread):

    def __init__(self, *args, **kwargs):
        super(Job, self).__init__(*args, **kwargs)
        # 用于暂停线程的标识
        self.__flag = threading.Event()
        # 设置为True
        self.__flag.set()
        # 用于停止线程的标识
        self.__running = threading.Event()
        # 将running设置为True
        self.__running.set()

    def run(self):
        while self.__running.isSet():
            self.__flag.wait()      # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
            time.sleep(1)

    def pause(self):
        self.__flag.clear()     # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set()    # 设置为True, 让线程停止阻塞

    def stop(self):
        self.__flag.set()       # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()        # 设置为False