#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Li Tian
@contact: litian_cup@163.com
@software: pycharm
@file: function_get.py
@time: 2021/1/16 14:18
@desc: 获取point_configures中的配置信息
"""
from dataclasses import dataclass
from point_test.configure_get import Configure
from point_test.mk_factory import MKFactory
from threading import Thread
from point_test.tip_time import TipTime


@dataclass
class GetDict:
    def __post_init__(self):
        self.cf = Configure('functions.ini')
        self.t = TipTime()
        self.mkf = MKFactory()
        self.data = {}
        self.names = None

    def generate_data(self, flag):
        self.names = self.cf.get_option(flag, 'indexs').split('-')
        for name in self.names:
            self.data[name] = ''

        return self.names, self.data

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
            xy, color = self.data.get(name)
            color_check_result = self.mkf.colorCheck(color, xy)

            if color_check_result:
                print('检测到了【对象】：', name)
                if operation == '0':
                    self.t.tip()
                elif operation == '1':
                    self.mkf.l1(xy)
                else:
                    self.mkf.ln(xy)

            self.t.tip('color')

    def func_demo(self):
        """功能1，双人御魂（一个电脑）"""
        check_result = self.check_settings()
        if not check_result:
            print('错误！配置流程中有没有配置的结点！')
            return

        if self.names is None:
            print('错误！还没有进行坐标配置！')
            return

        for name in self.names:
            t = Thread(target=self.run_thread, args=(name,), daemon=True, name='【线程】' + name)
            t.start()
            print(t.name)
