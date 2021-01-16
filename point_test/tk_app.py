#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Li Tian
@contact: litian_cup@163.com
@software: pycharm
@file: tk_app.py
@time: 2021/1/15 15:45
@desc: 可视化界面
        1. [pip迁移](https://blog.csdn.net/weixin_38781498/article/details/94037008)：pip install -r requirements.txt
"""
from dataclasses import dataclass
from tkinter import *
from tkinter import ttk
from point_test.configure_get import Configure
from point_test.function_get import GetDict
from system_hotkey import SystemHotkey
from point_test.mouse_action import MouseAction
from threading import Thread, enumerate, current_thread
from time import sleep


@dataclass
class App:

    def __post_init__(self):

        self.init_area()
        self.init_tk()

    def init_tk(self):
        """初始化tk"""
        self.font1 = (
            self.settings.get_option('font', 'font_type'),
            self.settings.get_option('font', 'font_size_1', 'int'))
        self.font_normal = (
            self.settings.get_option('font', 'font_type'),
            self.settings.get_option('font', 'font_size_normal', 'int'))

        self.root = Tk()
        self.root.title('狗贼v0.1')

        self.frame_1 = Frame(self.root)

        self.cmb1_value = StringVar()
        self.cmb2_value = StringVar()
        # 两个entry的值
        self.xy_value = StringVar()
        self.color_value = StringVar()

        # 标题
        # self.l_title = Label(self.root,
        #                      text='按【ALT+1】截取坐标和颜色',
        #                      fg=self.settings.get_option('gui', 'l_title_color'),
        #                      font=self.font1)
        # self.l_title.pack()

        self.l1 = Label(self.frame_1, text='选取功能和按键', font=self.font_normal)
        self.l1.pack(side=LEFT, fill=Y)

        self.cmb1 = ttk.Combobox(self.frame_1, textvariable=self.cmb1_value,
                                 width=self.settings.get_option('gui', 'cmb1_width', 'int'), font=self.font_normal)
        self.cmb1['values'] = ['【1】双人御魂（一个电脑）', '【2】待补充']
        # 选择第一个为默认
        # self.cmb1.current(0)
        self.cmb1.bind('<<ComboboxSelected>>', self.get_list)
        self.cmb1.pack(side=LEFT, fill=Y)

        self.cmb2 = ttk.Combobox(self.frame_1, textvariable=self.cmb2_value,
                                 width=self.settings.get_option('gui', 'cmb2_width', 'int'), font=self.font_normal)
        self.cmb2.bind('<<ComboboxSelected>>', self.get_key)
        self.cmb2.pack(side=LEFT, fill=Y)

        self.b_reset = Button(self.frame_1, text='保存当前到配置文件(S)', font=self.font_normal,
                              command=lambda: self.save_settings())
        self.b_reset.pack(side=LEFT, fill=BOTH, expand=YES)

        self.frame_xyc = Frame(self.root)

        self.l_xy = Label(self.frame_xyc, text='坐标', font=self.font_normal)
        self.l_xy.pack(side=LEFT, fill=Y)

        self.e_xy = Entry(self.frame_xyc, width=self.settings.get_option('gui', 'e_xy_length', 'int'),
                          textvariable=self.xy_value, font=self.font_normal, justify='center')
        self.e_xy.insert(END, self.xy)
        self.e_xy.pack(side=LEFT, fill=Y)

        self.l_c = Label(self.frame_xyc, text='颜色', font=self.font_normal)
        self.l_c.pack(side=LEFT, fill=Y)

        self.e_color = Entry(self.frame_xyc, width=self.settings.get_option('gui', 'e_color_length', 'int'),
                             textvariable=self.color_value, font=self.font_normal, justify='center')
        self.e_xy.insert(END, self.color)
        self.e_color.pack(side=LEFT, fill=Y)

        self.b4 = Button(self.frame_xyc, text='载入配置文件(L)', command=self.load_config, font=self.font_normal)
        self.b4.pack(side=LEFT, fill=BOTH, expand=YES)

        self.b1 = Button(self.frame_xyc, text='写入(W)', command=self.write_dict, font=self.font_normal)
        self.b1.pack(side=LEFT, fill=BOTH, expand=YES)

        self.b2 = Button(self.frame_xyc, text='运行(R)', command=self.run, font=self.font_normal)
        self.b2.pack(side=LEFT, fill=BOTH, expand=YES)

        self.b3 = Button(self.frame_xyc, text='退出(C)', command=self.destroy, font=self.font_normal)
        self.b3.pack(side=LEFT, fill=BOTH, expand=YES)

        self.frame_1.pack(side=TOP, fill=BOTH)
        self.frame_xyc.pack(side=BOTTOM, fill=BOTH)

    def init_area(self):
        """初始化区域"""
        # 全局快捷键设置
        self.xy, self.color = '', ''
        self.ma = MouseAction()
        self.hk = SystemHotkey()
        self.hk.register(('alt', 'w'), callback=lambda e: self.write_dict())
        self.hk.register(('alt', 'c'), callback=lambda e: self.destroy())
        self.hk.register(('alt', 'r'), callback=lambda e: self.func_start())

        # 配置初始化
        self.settings = Configure('config.ini')

        # 当前配置文件中的字典
        self.gd = GetDict()

    def run(self):
        self.check_mouse_move()
        self.root.mainloop()

    def get_list(self, *args):
        """获取对应下拉框的list，方便写入后续下拉框"""
        check_flag = self.cmb1_value.get()[1]
        self.cmb2['values'], self.current_dict = self.gd.generate_data(check_flag)

    def get_key(self, *args):
        """cmb2的对应的函数"""
        # return self.cmb2_value.get()
        ...

    def save_settings(self):
        """保存当前设置"""
        # 功能，功能节点names，data
        save_data = {
            'func_name': self.cmb1.get(),
            'names': self.cmb2['values'],
            'data': self.current_dict
        }
        # TODO

    def load_config(self):
        """载入数据"""
        ...

    def write_dict(self):
        """将信息写入到dict中"""
        aim_key = self.cmb2_value.get()
        aim_value = [self.xy, self.color]
        if aim_key != '':
            self.current_dict[aim_key] = aim_value
            print(self.current_dict)

    def get_postion_color(self):
        """设置绑定后的按键操作的值"""

        def extend_color(color: tuple):
            """将rgb颜色转换为rgb_16进制"""
            ten_six = "#%02x%02x%02x" % (color[0], color[1], color[2])
            return str(color) + '_' + ten_six, ten_six

        temp_xy = self.xy
        self.xy, self.color = self.ma.get_mouse_postion_color().get_info()

        if self.xy != temp_xy:
            self.e_xy.delete(0, END)
            self.e_xy.insert(END, str(self.xy))
            self.e_color.delete(0, END)
            insert_info, tensix = extend_color(self.color)
            self.e_color.insert(END, insert_info)
            return tensix

    def check_mouse(self):
        """循环检测鼠标"""
        while True:
            # 显示颜色设置
            tensix = self.get_postion_color()
            if tensix != '#-1-1-1':
                self.e_color.configure(fg=tensix)
            else:
                self.e_color.configure(fg='red')
            sleep(self.settings.get_option('mouse', 'mouse_check_speed', 'float'))

    def check_mouse_move(self):
        """检测鼠标移动，实时显示鼠标位置和颜色"""
        t = Thread(target=self.check_mouse)
        # 设置守护线程，主线程退出不必等待该线程
        t.setDaemon(True)
        t.start()

    def func_start(self):
        """运行"""
        self.gd.func_demo()

    def destroy(self):
        self.root.quit()


if __name__ == '__main__':
    App().run()
