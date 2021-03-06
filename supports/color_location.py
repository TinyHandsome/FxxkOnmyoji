#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Li Tian
@contact: litian_cup@163.com
@software: pycharm
@file: color_location.py
@time: 2021/1/30 10:41
@desc: 封装颜色和位置的信息作为点信息
"""

from dataclasses import dataclass


@dataclass
class Color:
    r: int
    g: int
    b: int

    def __post_init__(self):
        ...

    def get_values(self):
        return self.r, self.g, self.b


@dataclass
class Location:
    x: int
    y: int

    def __post_init__(self):
        ...

    def get_values(self):
        return self.x, self.y

@dataclass
class ColorLocation:
    c: Color = None
    l: Location = None

    def __post_init__(self):
        ...

    def set_color(self, c: Color):
        self.c = c

    def set_location(self, l: Location):
        self.l = l

    def set_color_location(self, c: Color, l: Location):
        self.set_color(c)
        self.set_location(l)

    def set_color_from_rgb(self, r, g, b):
        self.c = Color(r, g, b)

    def set_location_from_xy(self, x, y):
        self.l = Location(x, y)

    def set_color_location_from_values(self, r, g, b, x, y):
        self.set_color_from_rgb(r, g, b)
        self.set_location_from_xy(x, y)

    def get_color(self):
        """获取颜色数据"""
        return self.c.get_values()

    def get_loc(self):
        """获取坐标数据"""
        return self.l.get_values()

    def get_dict(self):
        """获取颜色位置数据"""
        return {'color': self.get_color(), 'loc': self.get_loc()}




