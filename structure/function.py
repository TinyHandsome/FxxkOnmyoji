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
        self.steps = []
        if self.step_infos is not None:
            # 如果是另一种初始化类的方式，则不用转换，否则将步骤转为Step类
            self.info2step()

    def init_function(self):
        """载入数据时，需要对各种字典进行初始化"""
        # 该功能下所有的点信息的名字-Point映射
        self.create_points_dict()

    def info2step(self):
        """根据step信息转为Step"""
        for info in self.step_infos:
            self.steps.append(Step(info))

    def create_points_dict(self):
        """在funciton中创建：根据func_name和point_name找到point的字典"""
        self.point_dict = {}
        for step in self.steps:
            for point in step.points:
                self.point_dict[point.point_name] = point

    def set_steps(self, steps: [Step]):
        """设置steps的信息"""
        self.steps = steps

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

    def get_point_names(self):
        """获取function中所有Point的名字"""
        points = []
        for s in self.steps:
            points += s.points
        return [p.point_name for p in points]

    def check_effective(self):
        """检查功能中所有的点信息都有，如果都没有则为无效，有一个有就运行这一个"""
        p_check_list = []
        for p in self.point_dict.values():
            p_check_list.append(p.point_info_check())

        if sum(p_check_list) == 0:
            """没有一个点是有效的"""
            return False
        else:
            return True

    @classmethod
    def get_function_from_dict(cls, function_dict: dict):
        """从json获取的dict字典中生成function"""
        new_steps = [Step.get_step_from_dict(s) for s in function_dict.pop('steps')]

        function_dict['step_infos'] = None
        function = Function(**function_dict)
        function.set_steps(new_steps)

        return function
