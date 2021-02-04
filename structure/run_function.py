#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Li Tian
@contact: litian_cup@163.com
@software: pycharm
@file: run_function.py
@time: 2021/2/4 15:16
@desc: 运行功能
"""

from dataclasses import dataclass
from structure.function import Function


@dataclass
class RunFunction:
    func: Function

    def __post_init__(self):
        ...

    def run_
