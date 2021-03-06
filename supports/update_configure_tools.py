#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Li Tian
@contact: litian_cup@163.com
@software: pycharm
@file: others.py
@time: 2021/2/8 15:47
@desc: 用于实现其他功能的软件，测试跟正式版本不同的那种
"""

from dataclasses import dataclass
from supports.configure_tools import Configure
from structure.function import Function
import os


@dataclass
class UpdateConfigureTools:
    is_test: False

    def __post_init__(self):
        path = 'configures/update_configs.ini'
        # 检查update_configs是否存在，不存在就创建，这里在Configure的类中已经实现了
        # check_file_exist(path)

        # 初始化update_configs.ini
        self.cf = Configure(path)

        # 检查里面特定的sec和opt是否存在，不存在则创建和初始化为空字符串
        self.cf.check_options({'updateConfigs': ['open_count'], 'lastOpen': ['last_open_funcname']})

    def show_my_words_at_first_open(self, open_immediately=False):
        """在软件第一次打开的时候，显示我的寄语"""
        # 获取cf中的值
        try:
            open_count = self.cf.get_option('updateConfigs', 'open_count', 'int')
        except Exception as e:
            open_count = 0

        if open_count < 1 or open_immediately:
            # 小于1 或者立刻打开为True 就显示
            os.startfile(os.path.join(os.getcwd(), 'configures/致软件使用者.html'))
        else:
            # 不然就啥都不干呗
            ...

        if self.is_test:
            # 测试的时候，将数字重置为0
            self.cf.update_value('updateConfigs', 'open_count', 0, True)
        else:
            # 如果不是测试，则更新次数
            open_count += 1
            # 更新软件打开次数
            self.cf.update_value('updateConfigs', 'open_count', str(open_count), True)

    def update_last_open_funcname(self, current_func: Function, load_file_name: str):
        """
        运行后记录该configure对应的功能
            1. 默认为-1
        """
        if load_file_name is not None:
            # 证明这次里面有导入的文件
            self.cf.update_value('lastOpen', load_file_name, current_func.func_name, True)
        else:
            # 没有导入，则直接记录到默认值里面
            self.cf.update_value('lastOpen', 'last_open_funcname', current_func.func_name, True)

    def get_last_open_funcname(self, load_file_name):
        """获取上次最后打开的功能名"""
        try :
            aim_name = self.cf.get_option('lastOpen', load_file_name)
            return aim_name
        except Exception as e:
            return self.cf.get_option('lastOpen', 'last_open_funcname')

