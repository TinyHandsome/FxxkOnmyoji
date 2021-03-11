#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Li Tian
@contact: litian_cup@163.com
@software: pycharm
@file: function.py
@time: 2021/2/2 14:17
@desc: 功能类，具有多个步骤，以及关联的功能
"""

from dataclasses import dataclass
from structure.step import Step


@dataclass
class Function:
    func_name: str
    func_code: str
    func_shown: int
    step_infos: [str]
    connections: [str]

    def __post_init__(self):
        self.point_dict = {}
        self.steps = []

        if self.step_infos is not None:
            # 如果是初始化的情况，需要将step_infos转为step
            self.info2step()
            # 建立点映射
            self.create_points_dict()

    def info2step(self):
        """根据step信息转为Step"""
        for info in self.step_infos:
            self.steps.append(Step(info))

    def create_points_dict(self):
        """在funciton中创建：根据func_name和point_name找到point的字典"""
        self.point_dict.clear()
        points = self.get_points()
        for point in points:
            self.point_dict[point.point_name] = point

    def set_steps(self, steps: [Step]):
        """设置steps的信息"""
        self.steps = steps

    def get_step_names(self):
        """获取该功能所有的step名字"""
        return [s.step_name for s in self.steps]

    def get_dict(self):
        steps_dict = [s.get_dict() for s in self.steps]
        function_dict = {
            'func_name': self.func_name,
            'func_code': self.func_code,
            'func_shown': self.func_shown,
            'steps': steps_dict,
            'connections': self.connections
        }
        return function_dict

    def update_point(self, point_name, loc, color):
        """更新该类中的点信息"""
        self.point_dict[point_name].update(loc, color)

    def get_points(self):
        """获取function中所有的point"""
        points = []
        for s in self.steps:
            points += s.points
        return points

    def get_point_names(self):
        """获取function中所有Point的名字"""
        points = self.get_points()
        return [p.point_name for p in points]

    def check_effective(self, return_num=False):
        """
        检查功能中所有的点信息都有，如果都没有则为无效，有一个有就运行这一个
            1. 注意：这里只检查基础流程有效点的数量，不检查连接流程
        """

        p_check_list = []
        for p in self.point_dict.values():
            p_check_list.append(p.check_effective())

        if return_num:
            # 是否返回有效点的数量
            return sum(p_check_list)
        else:
            if sum(p_check_list) == 0:
                """没有一个点是有效的"""
                return False
            else:
                # 否则返回有效点数量
                return True

    def check_connections_not_null(self):
        """检查connections是否为空"""
        if self.connections:
            return True
        else:
            return False

    @classmethod
    def get_function_from_dict(cls, function_dict: dict):
        """从json获取的dict字典中生成function"""
        new_steps = [Step.get_step_from_dict(s) for s in function_dict.pop('steps')]

        function_dict['step_infos'] = None
        function = Function(**function_dict)
        function.set_steps(new_steps)

        # 建立点映射
        function.create_points_dict()

        return function
