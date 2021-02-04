#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Li Tian
@contact: litian_cup@163.com
@software: pycharm
@file: function_factory.py
@time: 2021/1/18 14:47
@desc: 功能和数据模块
        [Python标记函数或类为废弃](https://blog.csdn.net/u013632755/article/details/106066972)
"""
from dataclasses import dataclass
import re
import json

from configure_tools import Configure
from color_location import ColorLocation


@dataclass
class Procedure:
    """
    流程，负责检测画面中是否出现目标区域，如果出现了，则点击一处或多处
    一个功能由多个流程组成，每个流程有：
        流程名
        流程字符串，即原始function.ini的字符串

    """
    proce_name: str
    # 【v0.3】重构了流程节点类，现在传入的是CL类而不是直接的loc和color值
    # 每一个流程有多个位置、颜色点，和多个点击点，点击点包含在位置颜色点中，根据流程名指定点击点
    cl: ColorLocation

    # TODO

    def __post_init__(self):
        # 【v0.3】是否新增下面代码，应该是不用的，重设位置和颜色的话，直接设cl的结果就行
        # self.proce_color = self.cl.get_color()
        # self.proce_loc = self.cl.get_loc()
        ...

    def reset_loc_color(self, loc, color):
        """设置loc和color"""
        self.cl.set_color_from_rgb(*color)
        self.cl.set_location_from_xy(*loc)
        # self.proce_loc = loc
        # self.proce_color = color

    def get_proce_name(self):
        """获取流程名"""
        return self.proce_name

    def get_values(self):
        """获取 流程名 [(坐标), (颜色)]"""
        return self.proce_name, [self.cl.get_loc(), self.cl.get_color()]


@dataclass
class Function:
    func_name: str
    procedures: [Procedure]

    def __post_init__(self):
        # 初始化一个 p_name: p的字典
        self.proce_dict = {}
        for p in self.procedures:
            self.proce_dict[p.get_proce_name()] = p

    def get_procedure_names(self):
        return [p.get_proce_name() for p in self.procedures]

    def get_func_name(self):
        return self.func_name

    def get_data(self):
        """获取data"""
        result = {}
        for p in self.procedures:
            k, v = p.get_values()
            result[k] = v
        return result

    def get_json(self):
        """获取字典"""
        result = self.get_data()

        json_data = {
            'func_name': self.func_name,
            'data': result
        }

        return json_data

    def update(self, p_name, p_xy, p_color):
        """更新值，需要更新是因为，后面是会改变流程节点的信息"""
        p = self.proce_dict.get(p_name)
        assert isinstance(p, Procedure)
        p.reset_loc_color(p_xy, p_color)

    def save_function_to_json(self, path):
        """保存配置文件function到json，【v0.3】弃用该函数"""
        # 【v0.3】更新后，单独的Function不具备保存功能，只有FuncFactory才能保存
        data = self.get_json()
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f)


@dataclass
class FuncFactory:
    """用于处理各个功能流程的读取、保存、更改等，不涉及具体实施，实施用function_tool"""

    def __post_init__(self):
        self.cf = Configure('configures/functions.ini')
        # function的列表，这里保存了所有的功能信息，也是读取和保存的点
        self.func_list = []

    def create_function_from_data(self, func_name, data):
        """
        普通创建function
        :param data: 流程名: CL的字典，一个功能的所有数据
        """
        procedures = []
        for k, cl in data.items():
            # k：流程节点名；cl：ColorLocation类
            # 【v0.3】Procedure初始化的方法改为对Colorlation处理
            # p = Procedure(k, cl[0], cl[1])
            p = Procedure(k, cl)
            procedures.append(p)
        return Function(func_name, procedures)

    def json2functions(self, json_var):
        """将json配置数据处理成Function列表"""

    def create_functionFactory_from_json(self, path):
        """从json中加载功能数据"""
        with open(path, "r", encoding="UTF-8") as f_load:
            json_var = json.load(f_load)
        func_name = json_var['func_name']
        data = json_var['data']

        return self.create_function_from_data(func_name, data)

    def init_function_from_name(self, func_name):
        """【v0.3：√】获取功能名，返回初始化的Function类"""
        # 获取功能名的编号，这里使用正则表达式
        pattern = re.compile(r'【(.*)】(.*)')
        # 获取功能名和编号
        code, f_name = re.search(pattern, func_name).groups()

        # 获取对应编号的流程名列表，并封装为Procedure
        procedure_names = self.cf.get_values(code)
        # 循环封装
        procedure_list = []
        for name in procedure_names:
            # 循环初始化一个功能的，每个节点的流程信息
            # 【v0.3】这里是初始化每个流程的坐标和时间信息，这里将初始化改为cl类
            procedure_list.append(Procedure(name, ColorLocation()))

        # 返回初始化的功能
        return Function(func_name, procedure_list)

    def get_func_names(self):
        """获取功能名称列表"""
        return self.cf.get_values('func_names')
