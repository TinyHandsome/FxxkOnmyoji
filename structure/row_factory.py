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
        for number, name, eef in zip(*current_func.get_step_names_effectives()):
            row = Row(number, name, eef)
            rows.append(row)

        self.rows = rows

    def clear_current_infos(self):
        """清除text中所有内容"""
        self.text.delete('1.0', 'end')

    def clear_write_line(self, start: str, line_number: int):
        """清除一行内容，写入一行内容"""
        self.clear_line(start)
        self.text.insert(start, row)

    def clear_line(self, start: str):
        """清除一行内容"""
        self.text.delete(start, 'line.end')

    def show_text(self, delete_all_before_insert=True):
        """将rows的信息显示在text组件上"""
        # 添加前是否清空内容
        if delete_all_before_insert:
            self.clear_current_infos()
        for row in self.rows:
            if not row.get_status():
                self.text.insert(row.get_start(), row.get_info(), 'tag_default_fg_red')
            else:
                self.text.insert(row.get_start(), row.get_info())
