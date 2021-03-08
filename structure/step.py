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


@dataclass()
class Step:
    # 步骤名为默认生成的step
    step_info: str

    def __post_init__(self):
        if self.step_info != '':
            # 如果初始化该类不是用的init，则step_info指定为''，此时不需要进行下面的操作，否则就需要进行
            self.generate_points_stepName()

    def __repr__(self):
        return str(self.points)

    def generate_points_stepName(self):
        self.points = []
        # 从步骤信息中获取步骤名和各点操作
        self.step_name, self.step_points = self.step_info.split('@')

        # 从多个点位信息中，开始遍历
        count = 0
        for point_info in self.step_points.split('-'):
            count += 1

            # 对每个点，进行点的类型和点击次数的获取，如果没有_，则点击次数为0，类型肯定为l或者n
            if '_' in point_info:
                info_list = point_info.split('_')
                point_type, click_times = info_list[0], info_list[1:]
            else:
                point_type = point_info
                click_times = [0]

            # 【v 0.32】名字前面加入编号
            def set_point_name():
                return self.step_name + '[' + str(count) + ']' + '@' + pt

            # 如果类型中没有m的话，即为c_1类型
            if point_type != 'm':
                pt = point_type
                point = Point('temp', pt, ('', ''), ('', '', ''), int(click_times[0]))
                point.point_name = set_point_name()
                self.points.append(point)
            else:
                # 否则需要建立多个点
                m_index = 0
                for c_times in click_times:
                    m_index += 1
                    pt = point_type + str(m_index)
                    point = Point('temp', pt, ('', ''), ('', '', ''), int(c_times))
                    point.point_name = set_point_name()
                    self.points.append(point)

    def get_dict(self):
        points_dict = [p.get_dict() for p in self.points]
        step_dict = {
            'step_name': self.step_name,
            'points': points_dict
        }
        return step_dict

    def get_location_points(self):
        """【v0.3，新增no-location】获取步骤中需要检查颜色的点"""
        l_points = []
        for p in self.points:
            # 在这里对不完善信息的点进行了过滤
            # 【v0.3 新增n的检查】
            if (p.check_type('l') or p.check_type('n')) and p.check_effective():
                l_points.append(p)

        return l_points

    def get_click_points(self):
        """获取步骤中需要点击的点"""
        c_points = []
        for p in self.points:
            # 在这里对不完善信息的点进行了过滤
            if p.check_type('c') and p.check_effective():
                c_points.append(p)

        return c_points

    def set_step(self, step_name: str, points: [Point]):
        """设置本类的step名字和点信息"""
        self.step_name = step_name
        self.points = points

    def check_effective(self):
        """
        检查该step是否是有效的，即是否都为空
            1. 步骤中所有点都有信息，就是有效的，这点跟function的不一样
            2. 只要有一个点没信息，step就是无效的
        """

        point_states = []
        for point in self.points:
            point_state = point.check_effective()
            point_states.append(point_state)

        if sum(point_states) == len(point_states):
            """所有都为True"""
            return True
        else:
            return False

    @classmethod
    def get_step_from_dict(cls, step_dict):
        """从step的字典中生成step"""
        step = Step('')

        points = []
        for point_dict in step_dict['points']:
            points.append(Point(**point_dict))

        step.set_step(step_dict['step_name'], points)
        return step
