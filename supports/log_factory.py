#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Li Tian
@contact: litian_cup@163.com
@software: pycharm
@file: log_factory.py
@time: 2021/3/11 15:59
@desc: 日志处理工厂
"""
import datetime
import os
from dataclasses import dataclass

from supports.functions import check_filefolder_exist


@dataclass
class LogFactory:
    def __post_init__(self):
        # 日记文件，一天一个，每次启动时删除七天前的文件
        self.current_time = datetime.datetime.now()
        self.current_date = datetime.datetime.strftime(self.current_time, '%Y-%m-%d')

        # 日志文件路径
        self.log_path = './logs/'
        # 需要检查日志文件夹是否存在，不存在，则自动生成
        check_filefolder_exist(self.log_path)

        # 创建日志文件
        log_file_name = self.current_date + '.txt'
        self.log_file = open(self.log_path + log_file_name, 'a+', encoding='utf-8')

    def clear_logs(self, keep_days):
        """清除7天前的日志数据"""
        delta_time = datetime.timedelta(days=keep_days)
        remove_date = self.current_time - delta_time

        count = 0
        for file_name in os.listdir(self.log_path):
            file_time = datetime.datetime.strptime(file_name.replace('.txt', ''), '%Y-%m-%d')
            if file_time < remove_date:
                os.remove(os.path.join(self.log_path, file_name))
                count += 1
        return count

    def write(self, info):
        """写入日志"""
        self.log_file.write(info)

    def close_log_file(self):
        """关闭日志文件"""
        self.log_file.close()
