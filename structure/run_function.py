#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Li Tian
@contact: litian_cup@163.com
@software: pycharm
@file: run_function.py
@time: 2021/2/4 15:16
@desc: 运行功能
"""

from dataclasses import dataclass
from structure.function import Function
from structure.function_factory import FunctionFactory
from structure.step import Step
from structure.point import Point
from supports.mk_factory import MKFactory
from supports.thread_management import ThreadManagement
from supports.tip_time import TipTime
from supports.info_pip import InfoPip
from supports.tip_time import TickTime


@dataclass
class RunFunction:
    func: Function
    ff: FunctionFactory
    tm: ThreadManagement
    info_stack: InfoPip

    def __post_init__(self):
        self.t = TipTime()
        self.mkf = MKFactory()
        # 暂停的标记，开始是不暂停
        self.pause_flag = False

    def run_step(self, step: Step):
        """运行一个步骤"""
        # 时间管理大师，每一个步骤，单独有一个时间管理
        self.tt = TickTime()

        # 【检查step中点的颜色】获取每个点的检查结果，如果标记带l的都是True则执行标记带c的点
        location_result = [self.check_point_color(p) for p in step.get_location_points()]

        # 【颜色都对，则运行有loc和color值的点】如果检查的结果都为True，则识别该流程被触发，执行点击事件
        if sum(location_result) == len(location_result):
            c_points = step.get_click_points()

            # 这里可能没有点信息
            if not c_points:
                # 【v0.3】这里应该不会执行，因为在[check_before_run]函数中已经进行了判断
                self.info_stack.info('步骤：' + step.step_name + '无效...', 2)
            else:
                # 时间检查，是否超时
                if self.tt.update_time_and_check():
                    # 超时返回的是True，结束叭，设置结束，并自己结束
                    self.info_stack.info('脚本检测超时，自动暂停所有功能', 2)
                    self.pause(shown_info=False)

                # 点击每一个需要click的点
                for cp in c_points:
                    self.click_points(cp)

        else:
            # 都不是True能怎么办，啥都不干呗
            ...

        # 监听频率
        self.t.tip('color')

    def check_point_color(self, point: Point):
        """【v0.3 需要根据l和n进行判断和返回】检查一个点的颜色"""
        xy, color = point.get_loc_color()
        p_type, p_times = point.get_type_click_time()
        color_check_result = self.mkf.colorCheck(color, xy)

        try:
            assert isinstance(color_check_result, bool)
            if 'l' in p_type:
                # l的话，该返回啥返回啥
                return color_check_result
            elif 'n' in p_type:
                # n的话，返回反过来的值
                return not color_check_result
            else:
                # 讲道理这种情况是不会出现的，可万一呢
                self.info_stack.info('狗贼！快联系管理员！', 2)
                return False
        except Exception as e:
            # 如果颜色不是bool的话，那么color_check_result就是结果和颜色
            self.info_stack.info(*color_check_result)
            return False

    def click_points(self, point: Point):
        """点击"""
        xy, color = point.get_loc_color()
        if point.click_times == '0':
            # 讲道理，这种情况是不会有的，万一有憨批呢，对吧
            ...
        elif point.click_times == '1':
            # 点击一次
            self.mkf.l1(xy)
        else:
            # 点击多次
            self.mkf.ln(xy)

    def run_function(self):
        """运行一个功能，包括多个步骤"""
        # 获取该功能的所有步骤和connections的所有步骤
        for s in self.ff.get_effective_steps(self.func):
            self.tm.build_thread(self.run_step, s.step_name, is_while=True, args=(s,))

    def pause(self, shown_info=True):
        """暂停"""

        # 需要暂停的线程，线程名不以_开头
        pause_threads = [p for p in self.tm.threads if not p.getName().replace('【线程】', '').startswith('_')]
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
                self.info_stack.info('功能' + self.func.func_name + '已暂停', 3)
        else:
            # 暂停了则继续
            self.pause_flag = False
            for t in pause_threads:
                t.resume()
            self.info_stack.info('功能' + self.func.func_name + '已恢复', 3)
