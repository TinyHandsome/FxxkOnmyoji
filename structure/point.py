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
    point_location: list or tuple
    point_color: list or tuple
    click_times: int

    def __post_init__(self):
        ...

    def get_type_click_time(self):
        """获取点的类型和点击次数"""
        return self.point_type, self.click_times

    def get_loc_color(self):
        """获取位置和颜色信息"""
        return self.point_location, self.point_color

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

    def update(self, loc, color):
        """重新设置loc和color"""
        self.point_location = loc
        self.point_color = color

    def check_type(self, p_type):
        """【v0.3，新增no-location】该点的类型是否是location/no-location，即检查颜色点"""
        if p_type in self.point_type:
            return True
        else:
            return False

    def check_effective(self):
        """自身点位信息检查，只要坐标和颜色有一个为空值则False"""
        if '' in self.point_location or '' in self.point_color:
            return False
        else:
            return True


