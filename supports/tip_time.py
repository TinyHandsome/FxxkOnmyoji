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
from datetime import datetime
from random import uniform, randrange
from supports.configure_tools import Configure


class TickTime:
    """存储一个流程的点击时间"""

    def __init__(self):
        conf = Configure('configures/configs.ini')
        # 获取多少时间内超过多少次算超时
        self.time_limit = conf.get_option('time', 'time_limit', 'int')
        self.count_limit = conf.get_option('time', 'count_limit', 'int')

        # 设置存放时间的list，这里因为检查次数为3，所以数组的长度为3
        self.init_time_list()

        # 当前统计的步骤名，如果步骤发生变化，则重新计时
        self.step_name = None

    def init_time_list(self):
        """初始化时间列表"""
        self.init_time = datetime.now()
        self.time_list = [self.init_time] * self.count_limit

    def check_time_if_timeout(self):
        """
        检查当前time_list中最新（第10次触发）到最旧时间（第一次触发）内，过了多久
        如果少于限制时间，那么触发频率过高，因此终止所有流程
        """
        new_time = self.time_list[-1]
        old_time = self.time_list[0]
        minus_seconds = (new_time - old_time).seconds

        # 时间对比，这里第一个时间不能是初始化的时间
        if old_time != self.init_time and minus_seconds < self.time_limit:
            # 触发5次竟然在10秒内，频率太快了，超时
            return True
        else:
            return False

    def update_time(self):
        """获取当前时间，并append到list的后面，然后获取最新10革时间点"""
        current_time = datetime.now()
        self.time_list.append(current_time)
        self.time_list = self.time_list[1:]

    def update_time_and_check(self, step_name):
        """综合获取时间和检查"""
        # 如果step_name为空  或者  step_name跟self.step_name相同，就开始记录和检查
        if step_name == self.step_name:
            self.update_time()
        else:
            # 如果step_name变了，则是在进行其他步骤，因此是正常的，所以重新初始化时间
            self.init_time_list()
        """
        最后不管是不是同样的步骤，都要更新步骤名，None跟不同名一样
        1. None：更新名字，初始化时间列表
        2. 同名：更新跟不更新无所谓
        3. 不同名：更新名字，并初始化时间列表
        """
        self.step_name = step_name
        return self.check_time_if_timeout()


class TipTime:
    def __init__(self):
        conf = Configure('configures/configs.ini')
        # 鼠标狂点时间间隔
        self.click_many_times_range = (conf.get_option('time', 'click_many_times_min', 'float'),
                                       conf.get_option('time', 'click_many_times_max', 'float'))
        # 颜色检测时间间隔
        self.color_check_range = (conf.get_option('time', 'color_check_min', 'float'),
                                  conf.get_option('time', 'click_many_times_max', 'float'))
        # 鼠标点击偏移量（上下左右）
        self.mouse_bias = conf.get_option('mouse', 'mouse_bias', 'int')

    def tip(self, flag='mouse'):
        """获取停顿时间"""
        if flag == 'mouse':
            aim_set = self.click_many_times_range

        elif flag == 'color':
            aim_set = self.color_check_range
        else:
            raise Exception('狗贼，时间有问题！')

        temp = uniform(aim_set[0], aim_set[1])
        time.sleep(temp)

    def sleep(self, seconds):
        """暂停时间"""
        time.sleep(seconds)

    def get_mouse_bias(self):
        """获取鼠标偏移量"""

        def gb():
            return randrange(-self.mouse_bias, self.mouse_bias)

        return gb(), gb()

    def get_times_randint(self, times):
        """获取点击次数的随机值"""
        return randrange(1, times)


if __name__ == '__main__':
    print(TipTime().get_mouse_bias())
