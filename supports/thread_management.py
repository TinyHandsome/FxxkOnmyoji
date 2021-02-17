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
from supports.tip_time import TickTime


@dataclass
class ThreadManagement:
    """线程管理"""

    def __post_init__(self):
        # 掌控所有的线程
        self.threads = []

    def build_thread(self, func, func_name, is_while=True, args=()):
        """建立线程"""
        t = Job(target=func, name='【线程】' + func_name, daemon=True, is_while=is_while, args=args)
        self.threads.append(t)
        # 设置守护线程，主线程退出不必等待该线程
        # print(t.name + '，启动...')
        t.start()


class Job(Thread):
    def __init__(self, target, name, daemon, is_while, args):
        super().__init__(name=name, daemon=daemon)
        self.target = target
        self.args = args
        self.is_while = is_while
        self.flag = Event()

        # 停止按钮
        self.stop_flag = False

        # 初始是打开的
        self.flag.set()

        # 时间管理大师
        self.tt = TickTime()
        # 是否需要时间管理
        self.is_check_tt = '_' not in name

    def run(self):
        if self.is_while:
            # 如果是循环检测线程，则一直循环
            while self.flag:
                # 如果检测到停止按钮，就直接退出
                if self.stop_flag:
                    break

                # 时间检查，是否超时
                if self.is_check_tt:
                    if self.tt.update_time_and_check():
                        # 超时返回的是True，结束叭，设置结束，并自己结束
                        self.stop()
                        print(self.name + '结束了')
                        break

                self.flag.wait()
                self.target(*self.args)
        else:
            self.target(*self.args)

    def pause(self):
        self.flag.clear()

    def resume(self):
        self.flag.set()

    def stop(self):
        self.stop_flag = True