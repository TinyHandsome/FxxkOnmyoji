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
import json

from configure_tools import Configure
from structure.function import Function


@dataclass
class FunctionFactory:

    def __post_init__(self):
        # 功能名映射功能的字典 工具
        self.function_dict = {}

    def init_functions_from_config(self):
        """从functions.ini文件中读取数据，获取初始化的[Function]"""
        cf = Configure('../configures/functions.ini')
        func_names = cf.get_values('func_names')

        functions = []
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
            # f_json = f.get_dict()
            functions.append(f)
        return functions

    def save_functions2json(self, functions: [Function], save_path):
        """将functions的list保存为json文件"""
        values_dict = [f.get_dict() for f in functions]
        with open(save_path, 'w', encoding='utf-8') as f:
            # 这里ensure_ascii表示是否要转为ascii码，不转则保存为中文
            json.dump(values_dict, f, indent=4, ensure_ascii=False)

    def load_functions_from_json(self, load_path):
        """读取json中的functions放到functions中"""
        with open(load_path, 'r', encoding='utf-8') as f:
            json_values = json.load(f)

        functions = [Function.get_function_from_dict(v) for v in json_values]
        for f in functions:
            f.init_function()

        return functions

    def create_functions_dict(self, functions: [Function]):
        """创建按一个从function_name到function的字典"""
        for f in functions:
            self.function_dict[f.func_code] = f

    def update(self, function_code, point_name, loc, color):
        """更新某个功能某个点位的位置和颜色"""
        self.function_dict[function_code].update_point(point_name, loc, color)


if __name__ == '__main__':
    test_ff = FunctionFactory()
    functions = test_ff.init_functions_from_config()

    # 测试初始化
    test_ff.save_functions2json(functions, '../templates/test_init.json')

    # 测试读取
    f = test_ff.load_functions_from_json('../templates/test_init.json')

    # 测试设置映射字典
    test_ff.create_functions_dict(f)
    test_ff.update('001', '挑战@lc_1', [1, 2], [1, 2, 3])

    print(f[0].func_name)
    print(f[0].steps[0].points)
