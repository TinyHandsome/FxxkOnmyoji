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
        self.rows = None

        # tag config
        self.text.tag_config('tag_default_fg_red', foreground='red')
        self.text.tag_config('tag_default_bg_yellow', background='yellow')

    def generate_row(self, current_func):
        """生成Row对象"""
        # 读取当前current_func的功能中各个step名
        rows = []
        for number, name, eef in current_func.get_step_names_effectives():
            row = Row(number, name, eef)
            rows.append(row)

        self.rows = rows

    def generate_name_line_dict(self):
        """生成一个对应关系 根据step名查找row，从而知道line"""
        name_row_dict = {}
        for row in self.rows:
            name_row_dict[row.info] = row
        return name_row_dict

    def clear_current_infos(self):
        """清除text中所有内容"""
        self.text.delete('1.0', 'end')

    def flush_run_step(self, step_name: str):
        """【v0.32 修改正在运行的step输出的text】高亮正在运行的step"""
        # 根据step_name找到row
        name_row_dict = self.generate_name_line_dict()
        aim_row = name_row_dict.get(step_name)

        # 删除row所在text行的信息
        self.clear_line(aim_row)
        # 将row的原始信息 加上running的buff
        self.show_row(aim_row, 'running')

    def clear_line(self, row: Row):
        """清除一行内容"""
        self.text.delete(row.get_start(), row.get_end())

    def show_row(self, row, show_type='default'):
        """显示一行内容"""
        # step无效，没配置，输出红色fg
        if not row.get_status():
            self.text.insert(row.get_start(), row.get_info(), 'tag_default_fg_red')
        # step有效，正在运行
        elif show_type == 'running':
            self.text.insert(row.get_start(), row.get_info(type_info='running', next_line=False), 'tag_default_bg_yellow')
        # step有效，没在运行
        else:
            self.text.insert(row.get_start(), row.get_info())

    def show_text(self, delete_all_before_insert=True):
        """将rows的信息显示在text组件上"""
        # 添加前是否清空内容
        if delete_all_before_insert:
            self.clear_current_infos()
        for row in self.rows:
            self.show_row(row)

    def flush(self, current_func):
        """初始化当前功能的步骤，并显示"""
        self.generate_row(current_func)
        self.show_text()
