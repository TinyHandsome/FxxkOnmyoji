#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Li Tian
@contact: litian_cup@163.com
@software: pycharm
@file: step.py
@time: 2021/2/2 14:17
@desc: 步骤的类，每个步骤可能会有多个点位信息
"""

from dataclasses import dataclass
from structure.point import Point


@dataclass
class Step:
    # 步骤名为默认生成的step
    step_info: str

    def __post_init__(self):
        self.points = []
        # 从步骤信息中获取步骤名和各点操作
        self.step_name, self.step_points = self.step_info.split('@')

        # 从多个点位信息中，开始遍历
        count = 0
        for point_info in self.step_points.split('-'):
            count += 1
            point_name = 'point_name_auto_generate_' + str(count)

            # 对每个点，进行点的类型和点击次数的获取，如果没有_，则点击次数为0，类型肯定为l
            if '_' in point_info:
                point_type, click_times = point_info.split('_')
            else:
                point_type = point_info
                click_times = 0
            point = Point(point_name, point_type, ('', ''), ('', '', ''), int(click_times))
            self.points.append(point)

    def get_dict(self):
        points_dict = [p.get_dict() for p in self.points]
        step_dict = {
            'step_name': self.step_name,
            'points': points_dict
        }
        return step_dict
