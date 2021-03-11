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
    info: str
    line: int

    def __post_init__(self):
        ...

