#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Li Tian
@contact: litian_cup@163.com
@software: pycharm
@file: row.py
@time: 2021/3/11 15:24
@desc: Text的每行
"""

from dataclasses import dataclass


@dataclass
class Row:
    line: int
    info: str
    # step是否是有效的
    status: bool

    def __post_init__(self):
        ...

    def get_start(self) -> str:
        """获得插入位置的行首"""
        return str(self.line) + '.0'

    def get_end(self) -> str:
        """获得插入位置的行尾"""
        return str(self.line) + '.end'

    def get_info(self, type_info='normal', next_line=True):
        """
        对原始数据进行处理
            1. 初始化写入的时候需要 回车
            2. 修改的时候不需要回车
        """
        # 非运行的step
        if type_info == 'normal':
            return '    ' + self.info + ('\n' if next_line else '')
        # 正在运行的step
        elif type_info == 'running':
            return '>   ' + self.info + ('\n' if next_line else '')

    def get_status(self):
        """获取是否有效"""
        return self.status
