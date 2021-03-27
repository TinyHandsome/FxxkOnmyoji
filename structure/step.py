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
            # 初始化后需要根据key获取步骤的类别
            self.set_step_key_type()

    def __repr__(self):
        return str(self.points)

    def generate_points_stepName(self):
        self.points = []
        # 从步骤信息中获取步骤名和各点操作
        self.step_key, self.step_value = self.step_info
        self.step_name, self.step_points = self.step_value.split('@')

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
            def set_point_name(pt):
                return self.step_name + '[' + str(count) + ']' + '@' + pt

            def get_temp_point(pt, c_time):
                p = Point('temp', pt, ('', ''), ('', '', ''), c_time)
                p.point_name = set_point_name(pt)
                self.points.append(p)

            if point_type == 'm':
                # 如果类型为多重点击
                m_index = 0
                for c_times in click_times:
                    m_index += 1
                    pt = point_type + str(m_index)
                    get_temp_point(pt, int(c_times))
            elif point_type == 'pr':
                # 如果类型为press release型，拖动滑动条
                pt = 'p'
                get_temp_point(pt, 0)
                pt = 'r'
                get_temp_point(pt, 0)
            elif point_type == 'pause':
                # 如果类型为pause型，则执行暂停
                pt = 'pause'
                get_temp_point(pt, int(click_times[0]))
            else:
                # 否则为c_1类型
                pt = point_type
                get_temp_point(pt, int(click_times[0]))

    def set_step_key_type(self):
        """根据step_key获取类别，一般为step1、step2这种的"""
        keys = self.step_key.split('_')
        if len(keys) > 1:
            # 如果大于1，则有类别
            self.step_type = keys[-1]
        else:
            self.step_type = ''

    def get_dict(self):
        points_dict = [p.get_dict() for p in self.points]
        step_dict = {
            'step_name': self.step_name,
            'step_type': self.step_type,
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

    def get_click_points(self, p_type='c'):
        """获取步骤中需要点击的点"""
        points = []
        for p in self.points:
            # 在这里对不完善信息的点进行了过滤
            if p.check_type(p_type) and p.check_effective():
                points.append(p)

        return points

    def set_step(self, step_name: str, step_type: str, points: [Point]):
        """设置本类的step名字和点信息"""
        self.step_name = step_name

        if step_type:
            self.step_type = step_type
        else:
            # 为None的话置为空
            self.step_type = ''

        self.points = points

    def get_name_effective(self):
        """返回名字和与否"""
        return self.step_name, self.check_effective()

    def check_effective(self):
        """
        检查该step是否是有效的，即是否都为空
            1. 步骤中所有点都有信息，就是有效的，这点跟function的不一样
            2. 只要有一个点没信息，step就是无效的
            3. 如果点的类型是pause则可以跳过检查
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

    def is_step_check(self):
        """
        返回该step是否需要检查
            1. u类型的不需要进行 重复检查
        """
        if 'u' in self.step_type:
            return False
        else:
            return True

    @classmethod
    def get_step_from_dict(cls, step_dict):
        """从step的字典中生成step"""
        step = Step('')

        points = []
        for point_dict in step_dict['points']:
            points.append(Point(**point_dict))

        step.set_step(step_dict.get('step_name'), step_dict.get('step_type'), points)
        return step

