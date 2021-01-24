#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Li Tian
@contact: litian_cup@163.com
@software: pycharm
@file: function_tools.py
@time: 2021/1/16 14:18
@desc: 获取point_configures中的配置信息
"""
from dataclasses import dataclass
from mk_factory import MKFactory
from tip_time import TipTime
from function_factory import Function
from methods import build_thread


@dataclass
class FuncRun:
    func: Function

    def __post_init__(self):
        self.t = TipTime()
        self.mkf = MKFactory()

        # 配置文件：名字：(坐标，颜色)
        self.data = self.func.get_data()
        # 配置文件：[名字]
        self.names = self.func.get_procedure_names()
        # 当前事件信息
        self.current_info = None

    def check_settings(self):
        """检查流程设置的字典中是否有空值"""
        for v in self.data.values():
            if v == '':
                return False
        return True

    def run_thread(self, name):
        """每一个颜色检查是独立的，检测到了就执行相应的操作"""
        operation = name.split('_')[-1]
        while True:
            # 获取目标流程节点的坐标和颜色
            xy, color = self.data.get(name)
            try:
                # 获取颜色检查
                color_check_result = self.mkf.colorCheck(color, xy)
            except Exception as e:
                # self.current_info = ('流程不完整', 'red')
                return

            if isinstance(color_check_result, str):
                # 如果颜色检测的过程中出现了错误， 则返回的肯定是str字符串
                self.current_info = color_check_result
                return

            # 如果返回的不是字符串，则返回的是False或者True
            if color_check_result:
                # print('检测到了【对象】：', name)
                if operation == '0':
                    # 操作为0，即，检测到了不操作，暂停一会儿
                    self.t.tip()
                elif operation == '1':
                    # 点击一次
                    self.mkf.l1(xy)
                else:
                    # 点击多次
                    self.mkf.ln(xy)

            # 颜色检查频率
            self.t.tip('color')

    def func_demo(self):
        """功能1，双人御魂（一个电脑），识别到了颜色就点击"""
        check_result = self.check_settings()
        if not check_result:
            return '错误！配置流程中有没有配置的结点！', 'red'

        try:
            for name in self.names:
                build_thread(self.run_thread, name, (name,))

            return
        except Exception as e:
            return '流程启动失败...', 'red'
