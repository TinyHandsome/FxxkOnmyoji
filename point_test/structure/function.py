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
        # 将步骤转为Step类
        self.steps = []
        self.info2step()

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

    def info2step(self):
        """根据step信息转为Step"""
        for info in self.step_infos:
            self.steps.append(Step(info))
