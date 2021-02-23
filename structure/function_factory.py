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
        1. 无论导入json还是新建了初始化，都需要建立code-function和name-function的映射关系
"""

from dataclasses import dataclass
import re
import json
import pyperclip

from supports.configure_tools import Configure
from structure.function import Function, Step


@dataclass
class FunctionFactory:

    def __post_init__(self):
        # 功能名映射功能的字典 工具
        self.function_dict_by_code = {}
        self.function_dict_by_name = {}

    def init_functions_from_config(self):
        """从functions.ini文件中读取数据，获取初始化的[Function]"""
        cf = Configure('configures/functions.ini')
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
            functions.append(f)

        # 初始化functiondict
        self.create_functions_dict(functions)
        return functions

    def get_dict_from_functions(self, functions: [Function]):
        """将functions转为dict"""
        return [f.get_dict() for f in functions]

    def get_json_from_functions(self, functions: [Function]):
        """【测试专用】获取functions的json，并放到粘贴板"""
        info = json.dumps(self.get_dict_from_functions(functions), indent=4, ensure_ascii=False)
        pyperclip.copy(info)
        print('json信息已经复制到粘贴板')
        return info

    def save_functions2json(self, functions: [Function], save_path):
        """将functions的list保存为json文件"""
        values_dict = self.get_dict_from_functions(functions)
        with open(save_path, 'w', encoding='utf-8') as f:
            # 这里ensure_ascii表示是否要转为ascii码，不转则保存为中文
            json.dump(values_dict, f, indent=4, ensure_ascii=False)

    def load_functions_from_json(self, load_path):
        """读取json中的functions放到functions中"""
        with open(load_path, 'r', encoding='utf-8') as f:
            json_values = json.load(f)

        functions = [Function.get_function_from_dict(v) for v in json_values]

        # 初始化functiondict
        self.create_functions_dict(functions)

        return functions

    def create_functions_dict(self, functions: [Function]):
        """创建按一个从function_name到function的字典"""
        # 创建的时候，需要清空所有的字典
        self.function_dict_by_code.clear()
        self.function_dict_by_name.clear()
        for f in functions:
            self.function_dict_by_code[f.func_code] = f
            self.function_dict_by_name[f.func_name] = f

    def get_function_names(self) -> list:
        """获取所有功能的名字"""
        values = [(f.func_shown, f.func_name) for func_name, f in self.function_dict_by_name.items()]
        show_func_names = []
        for shown, name in values:
            if shown == 1:
                show_func_names.append(name)
        return show_func_names

    def get_function_from_function_name(self, func_name) -> Function:
        """根据功能名获取功能对象"""
        return self.function_dict_by_name[func_name]

    def get_steps(self, func: Function) -> [Step]:
        """获取该功能的所有步骤和connections的所有步骤"""
        steps = func.steps

        # 关联的function
        for code in func.connections:
            temp_f = self.function_dict_by_code.get(code)
            steps += temp_f.steps

        return steps

    def get_effective_steps(self, func: Function) -> [Step]:
        """获取该功能的所有步骤和connections有效步骤"""
        return [s for s in self.get_steps(func) if s.check_effective()]

    def check_funcname(self, funcname):
        """【暂时没用到】检查功能名是否在当前功能列表中"""
        for fn in self.function_dict_by_name.keys():
            if fn == funcname:
                return True

        return False

    def set_functions_func(self, functions: [Function], func: Function):
        """如果func的funcname在functions中有，则设置functions的func_name的function为func"""
        result_functions = []
        for f in functions:
            if f.func_name == func.func_name and f.check_effective(True) <= func.check_effective(True):
                result_functions.append(func)
            else:
                result_functions.append(f)

        return result_functions


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

    # 获取所有的功能
    function_names = test_ff.get_function_names()
    print(function_names)
    # 获取某一个功能的步骤
    print(test_ff.get_step_names_from_function_name(function_names[0]))
