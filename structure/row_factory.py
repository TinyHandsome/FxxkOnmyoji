#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Li Tian
@contact: litian_cup@163.com
@software: pycharm
@file: row_factory.py
@time: 2021/3/11 15:50
@desc: 行处理工厂
"""

from dataclasses import dataclass
from tkinter import Text

from structure.row import Row


@dataclass
class RowFactory:
    text: Text

    def __post_init__(self):
        ...

    def generate_row(self, current_func):
        """生成Row对象"""
        # 读取当前current_func的功能中各个step名
        step_names = current_func.get_step_names()
        rows = []
        for sn in range(len(step_names)):
            row = Row(step_names[sn], sn + 1)
            rows.append(row)
