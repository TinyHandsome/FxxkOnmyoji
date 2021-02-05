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
from structure.step import Step
from structure.point import Point
from supports.mk_factory import MKFactory
from supports.tip_time import TipTime
from supports.methods import build_thread


@dataclass
class RunFunction:
    func: Function

    def __post_init__(self):
        self.t = TipTime()
        self.mkf = MKFactory()

        self.temp_info = '', 0

    def run_step(self, step: Step):
        """运行一个步骤"""
        # 获取每个点的检查结果，如果标记带l的都是True则执行标记带c的点
        location_result = [self.check_point_color(p) for p in step.get_location_points()]

        # 如果检查的结果都为True，则识别该流程被触发，执行点击事件
        if sum(location_result) == len(location_result):
            c_points = step.get_click_points()
            for cp in c_points:
                self.click_points(cp)
        else:
            # 都不是True能怎么办，啥都不干呗
            ...

        # 监听频率
        self.t.tip('color')

    def check_point_color(self, point: Point):
        """检查一个点的颜色"""
        xy, color = point.get_loc_color()
        # p_type, p_times = point.get_type_click_time()
        color_check_result = self.mkf.colorCheck(color, xy)

        try:
            assert isinstance(color_check_result, bool)
        except Exception as e:
            self.temp_info = color_check_result
            print(self.temp_info)
            return False

        return color_check_result

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
        for s in self.func.steps:
            build_thread(self.run_step(s), s.step_name)
