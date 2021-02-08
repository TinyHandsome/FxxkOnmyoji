#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Li Tian
@contact: litian_cup@163.com
@software: pycharm
@file: thread_management.py
@time: 2021/1/18 17:42
@desc: 常用methods
        1. [线程的关闭](https://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread)
"""
from threading import Thread, Event
from dataclasses import dataclass


@dataclass
class ThreadManagement:
    """线程管理"""

    def __post_init__(self):
        # 掌控所有的线程
        self.threads = []

    def build_thread(self, func, func_name, args=()):
        """建立线程"""
        t = Job(target=func, name='【线程】' + func_name, daemon=True, args=args)
        self.threads.append(t)
        # 设置守护线程，主线程退出不必等待该线程
        # print(t.name + '，启动...')
        t.start()


class Job(Thread):
    def __init__(self, target, name, daemon, args):
        super().__init__(name=name, daemon=daemon)
        self.target = target
        self.args = args
        self.flag = Event()

        # 初始是打开的
        self.flag.set()

    def run(self):
        while self.flag:
            self.flag.wait()
            self.target(*self.args)

    def pause(self):
        self.flag.clear()

    def resume(self):
        self.flag.set()
