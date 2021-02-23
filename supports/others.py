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
import os


@dataclass
class Others:
    is_test: False

    def __post_init__(self):
        self.cf = Configure('configures/update_configs.ini')

    def show_my_words_at_first_open(self, open_immediately=False):
        """在软件第一次打开的时候，显示我的寄语"""
        # 获取cf中的值
        open_count = self.cf.get_option('updateConfigs', 'open_count', 'int')
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
