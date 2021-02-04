#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Li Tian
@contact: litian_cup@163.com
@software: pycharm
@file: configure_tools.py
@time: 2021/1/16 10:54
@desc: 一些配置文件
        1. [python之atexit模块的使用](https://www.cnblogs.com/wanghuixi/p/11254304.html)
"""

import configparser
from dataclasses import dataclass


@dataclass
class Configure:
    path: str

    def __post_init__(self):
        self.conf = configparser.ConfigParser()
        self.conf.read(self.path, encoding='utf-8')
        self.sections = self.conf.sections()

    def get_options(self, sec):
        """获取section中的所有option"""
        return self.conf.options(sec)

    def get_values(self, sec):
        """获取secion中的的所有values"""
        _, values = zip(*self.get_items(sec))
        return values

    def get_items(self, sec):
        """获取section中所有的键值对"""
        return self.conf.items(sec)

    def get_option(self, sec, opt, opt_type='str'):
        """获取section中option的值，默认得到的值为str"""
        if opt_type == 'int':
            return self.conf.getint(sec, opt)
        elif opt_type == 'float':
            return self.conf.getfloat(sec, opt)
        elif opt_type == 'bool':
            return self.conf.getboolean(sec, opt)
        else:
            return self.conf.get(sec, opt)

    def print_test(self):
        """测试输出"""
        print(self.conf.sections())


if __name__ == '__main__':
    cf = Configure('configures/functions.ini')
    print(cf.get_values('func_names'))
