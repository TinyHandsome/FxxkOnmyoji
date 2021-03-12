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

from supports.functions import check_file_exist


@dataclass
class Configure:
    path: str

    def __post_init__(self):
        # 如果路径ini不存在，则创建该ini
        check_file_exist(self.path)
        self.conf = configparser.ConfigParser()
        self.conf.read(self.path, encoding='utf-8')
        self.sections = self.conf.sections()

    def check_options(self, so_dict: dict):
        """检查section的option是否存在， seciont: [option]"""
        for sec, opts in so_dict.items():
            for opt in opts:
                try:
                    self.get_option(sec, opt)
                except Exception as e:
                    # 没有的话初始化为空字符串
                    self.update_value(sec, opt, '')

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

    def update_value(self, sec, opt, value, is_save=True):
        """修改结果"""
        if not self.conf.has_section(sec):
            # 没有sec的话，新建一个sec
            self.conf.add_section(sec)

        self.conf.set(sec, opt, value)

        if is_save:
            with open(self.path, 'w', encoding='utf-8') as config_file:
                self.conf.write(config_file)

    def print_test(self):
        """测试输出"""
        print(self.conf.sections())


if __name__ == '__main__':
    cf = Configure('../configures/asd.ini')
    cf.check_options({'updateConfigs': ['open_count'], 'lastOpen': ['last_open_funcname']})
    # cf.update_value('others', 'open_count', '0', True)
