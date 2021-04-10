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

from supports.info_pip import InfoPip
from supports.tip_time import TipTime


@dataclass
class ThreadManagement:
    """线程管理"""
    info_stack: InfoPip

    def __post_init__(self):
        # 掌控所有的线程
        self.threads = []
        # 暂停的标记，开始是不暂停
        self.pause_flag = False
        # 暂停时间
        self.t = TipTime()
        # 进程控制，保证只有一个在运行
        self.lock = Event()
        self.lock.set()

    def get_all_threads(self):
        """查看所有线程"""
        return self.threads

    def get_need_threads(self):
        """获取不以_开头的线程"""
        return [p for p in self.threads if not p.ignore_type]

    def clear_not_ignored_threads(self):
        """清除不需要忽略的线程"""
        # 停止已有的线程
        for p in self.get_need_threads():
            p.stop()
        # 清空线程
        self.threads.clear()

    def build_thread(self, func, func_name, is_while=True, args=()):
        """建立线程"""
        t = Job(target=func, name='【线程】' + func_name, tip=self.t, lock=self.lock, daemon=True, is_while=is_while,
                args=args)
        self.threads.append(t)
        # 设置守护线程，主线程退出不必等待该线程
        # print(t.name + '，启动...')
        t.start()

    def stop(self):
        """停止"""
        stop_threads = self.get_need_threads()
        if len(stop_threads) != 0:
            for t in stop_threads:
                t.stop()

    def pause(self, func_name, shown_info=True):
        """暂停"""

        # 需要暂停的线程，线程名不以_开头
        pause_threads = self.get_need_threads()
        # 如果没有需要暂停的线程，即没有启动啥功能，则报错
        if len(pause_threads) == 0:
            self.info_stack.info('你啥也没启动啊，暂停个鬼啊', 2)
            return

        if not self.pause_flag:
            # 未暂停
            self.pause_flag = True
            for t in pause_threads:
                t.pause()
            if shown_info:
                self.info_stack.info('功能' + func_name + '已暂停', 3)
        else:
            # 暂停了则继续
            self.pause_flag = False
            for t in pause_threads:
                t.resume()
            self.info_stack.info('功能' + func_name + '已恢复', 3)


class Job(Thread):
    def __init__(self, target, name, tip, lock, daemon, is_while, args):
        super().__init__(name=name, daemon=daemon)
        self.target = target
        self.tip = tip
        self.lock = lock
        self.args = args
        self.is_while = is_while
        self.flag = Event()

        # 是否是_开头的线程，是的话，不需要停顿
        self.ignore_type = self.name.replace('【线程】', '').startswith('_')

        # 停止按钮
        self.stop_flag = False

        # 初始是打开的
        self.flag.set()

    def run(self):
        if self.is_while:
            # 如果是循环检测线程，则一直循环
            while True:
                # 如果检测到停止按钮，就直接退出
                if self.stop_flag:
                    break

                # 运行时锁住
                self.lock.wait()
                self.lock.clear()

                self.flag.wait()
                self.target(*self.args)

                self.lock.set()
                # 如果不是_开头的线程，就要停会儿在运行哦
                if not self.ignore_type:
                    # 暂停一会儿再释放
                    self.tip.tip('color')
        else:
            self.target(*self.args)

    def pause(self):
        self.flag.clear()

    def resume(self):
        self.flag.set()

    def stop(self):
        self.stop_flag = True
