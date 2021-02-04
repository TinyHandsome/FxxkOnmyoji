#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Li Tian
@contact: litian_cup@163.com
@software: pycharm
@file: point.py
@time: 2021/2/2 14:17
@desc: 点位信息的类
"""

from dataclasses import dataclass


@dataclass
class Point:
    point_name: str
    point_type: str
    point_location: tuple
    point_color: tuple
    click_times: int

    def __post_init__(self):
        self.x = self.point_location[0]
        self.y = self.point_location[1]
        self.r = self.point_color[0]
        self.g = self.point_color[1]
        self.b = self.point_color[2]

    def get_dict(self):
        """将点位的所有信息转化为字典格式"""
        point_dict = {
            "point_name": self.point_name,
            "point_type": self.point_type,
            "point_location": self.point_location,
            "point_color": self.point_color,
            "click_times": self.click_times
        }
        return point_dict

