#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Li Tian
@contact: litian_cup@163.com
@software: pycharm
@file: function_factory.py
@time: 2021/2/2 14:39
@desc: 功能操作工厂：初始化功能模块给tk，保存，加载等
"""

from dataclasses import dataclass
import re

from configure_tools import Configure
from structure.function import Function


@dataclass
class FunctionFactory:

    def __post_init__(self):
        ...

    def init_functions_from_config(self):
        """从functions.ini文件中读取数据，获取初始化的[Function]"""
        cf = Configure('../configures/functions.ini')
        func_names = cf.get_values('func_names')

        pattern = re.compile(r'【(_?)(\d+)】(.*)')
        for fn in func_names:
            shown, code, name = re.search(pattern, fn).groups()
            shown = 0 if shown == '_' else 1

            step_infos = []
            connections = []

            for key, value in cf.get_items(code):
                if key != 'connections':
                    step_infos.append(value)
                else:
                    connections = value.split('-')

            f = Function(name, code, shown, step_infos, connections)
            f_json = f.get_dict()
            print(f_json)



if __name__ == '__main__':
    test_ff = FunctionFactory()
    test_ff.init_functions_from_config()
