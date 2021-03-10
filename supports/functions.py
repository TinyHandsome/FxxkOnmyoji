#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Li Tian
@contact: litian_cup@163.com
@software: pycharm
@file: functions.py
@time: 2021/2/23 13:43
@desc: 一些小工具函数
"""
import os


def get_files_names(files):
    """
    通过文件路径，获取没有后缀的文件名
        1. files:list，返回list
        2. files:str，返回str
    """
    if isinstance(files, str):
        file_name = os.path.basename(files)
        file_name_without_suffix = file_name.split('.')[0]
        return file_name_without_suffix
    elif isinstance(files, (list, tuple)):
        file_name_without_suffixs = []
        for file in files:
            file_name_without_suffixs.append(get_files_names(file))
        return file_name_without_suffixs
    else:
        print(type(files))
        print('咋肥四鸭？')


def check_filefolder_exist(filefolder):
    """检查文件夹是否存在，否则创建该目录"""
    if not os.path.exists(filefolder):
        os.makedirs(filefolder)
