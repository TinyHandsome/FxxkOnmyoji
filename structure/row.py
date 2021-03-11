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
        """获得插入的位置"""
        return str(self.line) + '0.1'

    def get_info(self, type_info='normal'):
        """对原始数据进行处理"""
        if type_info == 'normal':
            return '    ' + self.info + '\n'
        elif type_info == 'running':
            return '==> ' + self.info + '\n'

    def get_status(self):
        """获取是否有效"""
        return self.status
