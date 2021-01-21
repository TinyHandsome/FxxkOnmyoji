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
        2. [Python3入门之线程threading常用方法](https://www.cnblogs.com/chengd/articles/7770898.html)
        3. [threading之线程的开始,暂停和退出](https://www.cnblogs.com/cnhyk/p/13697121.html)
"""
from dataclasses import dataclass
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from configure_tools import Configure
from function_tools import FuncRun
from system_hotkey import SystemHotkey
from mouse_action import MouseAction
from function_factory import FuncFactory
from time import sleep
from set_windows import SetWin
from methods import build_thread


@dataclass
class App:

    def __post_init__(self):

        self.global_var()
        self.init_area()
        self.init_tk()

    def global_var(self):
        """全局变量初始化"""

        # 初始坐标和颜色
        self.xy, self.color = '', ''
        # 初始化功能信息
        self.func = None

    def init_tk(self):
        """初始化tk"""
        self.font1 = (
            self.settings.get_option('font', 'font_type'),
            self.settings.get_option('font', 'font_size_1', 'int'))
        self.font_normal = (
            self.settings.get_option('font', 'font_type'),
            self.settings.get_option('font', 'font_size_normal', 'int'))

        self.root = Tk()
        # 置顶
        self.root.wm_attributes('-topmost', 1)
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
        # TODO，这里需要修改配置
        self.cmb1['values'] = self.ff.get_func_names()
        # 选择第一个为默认
        # self.cmb1.current(0)
        self.cmb1.bind('<<ComboboxSelected>>', self.get_list)
        self.cmb1.pack(side=LEFT, fill=Y)

        self.cmb2 = ttk.Combobox(self.frame_1, textvariable=self.cmb2_value,
                                 width=self.settings.get_option('gui', 'cmb2_width', 'int'), font=self.font_normal)
        self.cmb2.bind('<<ComboboxSelected>>', self.get_key)
        self.cmb2.pack(side=LEFT, fill=Y)

        self.b2 = Button(self.frame_1, text='运行(r)', command=self.func_start, font=self.font_normal)
        self.b2.pack(side=LEFT, fill=BOTH, expand=YES)

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

        self.b_adjust_win = Button(self.frame_xyc, text='调整界面(d)', font=self.font_normal,
                                   command=self.set_two_win_left)
        self.b_adjust_win.pack(side=LEFT, fill=BOTH, expand=YES)

        self.b4 = Button(self.frame_xyc, text='暂停(p)', command=self.pause, font=self.font_normal)
        self.b4.pack(side=LEFT, fill=BOTH, expand=YES)

        self.b3 = Button(self.frame_xyc, text='退出(c)', command=self.destroy, font=self.font_normal)
        self.b3.pack(side=LEFT, fill=BOTH, expand=YES)

        self.frame_2 = Frame(self.root)

        self.b1 = Button(self.frame_2, text='写入信息(w)', command=self.write_dict, font=self.font_normal)
        self.b1.pack(side=LEFT, fill=BOTH, expand=YES)

        self.b_save_conf = Button(self.frame_2, text='保存为默认(s)', font=self.font_normal,
                                  command=lambda: self.save_config_as_default())
        self.b_save_conf.pack(side=LEFT, fill=BOTH, expand=YES)

        self.b_save_conf = Button(self.frame_2, text='保存到文件(S)', font=self.font_normal,
                                  command=...)  # TODO
        self.b_save_conf.pack(side=LEFT, fill=BOTH, expand=YES)

        self.b4 = Button(self.frame_2, text='载入默认配置(l)', command=self.load_default_config, font=self.font_normal)
        self.b4.pack(side=LEFT, fill=BOTH, expand=YES)

        self.b5 = Button(self.frame_2, text='选择配置文件(L)', command=self.load_user_config, font=self.font_normal)
        self.b5.pack(side=LEFT, fill=BOTH, expand=YES)

        self.frame_1.pack(side=TOP, fill=BOTH)
        self.frame_xyc.pack(side=TOP, fill=BOTH)
        self.frame_2.pack(side=TOP, fill=BOTH)

    def init_area(self):
        """初始化区域"""
        # 全局快捷键设置
        self.hk = SystemHotkey()
        self.hk.register(('alt', 'w'), callback=lambda e: self.write_dict())
        self.hk.register(('alt', 'c'), callback=lambda e: self.destroy())
        self.hk.register(('alt', 'r'), callback=lambda e: self.func_start())
        self.hk.register(('alt', 'p'), callback=lambda e: self.pause())
        self.hk.register(('alt', 's'), callback=lambda e: self.save_config_as_default())
        self.hk.register(('alt', 'l'), callback=lambda e: self.load_default_config())
        self.hk.register(('alt', 'd'), callback=lambda e: self.set_two_win_left())
        self.hk.register(('alt', 'shift', 'l'), callback=lambda e: self.load_user_config())

        # 移动鼠标
        self.ma = MouseAction()
        # 配置初始化
        self.settings = Configure('configures/config.ini')
        # 设置初始界面
        self.sw = SetWin()
        # 操作功能配置文件的工具
        self.ff = FuncFactory()

    def set_two_win_left(self):
        """设置两个阴阳师的界面排在左边"""
        self.win_settings = self.settings.get_items('windows')
        handles = self.sw.find_onmyoji_handle()

        # 遍历阴阳师所有句柄
        for h in range(len(handles)):
            # 提取第h个坐标，h只有1的话，就只提取一个坐标
            loc = [int(temp) for temp in self.win_settings[h][1].split(',')]
            try:
                self.sw.move_rect(handles[h], loc)
                print('成功调整界面！')
            except Exception as e:
                print('错误！未打开阴阳师！')

    def run(self):
        self.check_mouse_move()
        self.root.mainloop()

    def get_list(self, *args):
        """获取对应下拉框的list，方便写入后续下拉框"""
        cmb1_v = self.cmb1_value.get()
        self.func = self.ff.init_config(cmb1_v)
        # 设置下拉框的值
        self.cmb2['values'] = self.func.get_procedure_names()

    def get_key(self, *args):
        """cmb2的对应的函数"""
        # return self.cmb2_value.get()
        ...

    def save_config_as_default(self):
        """保存当前设置"""
        try:
            self.func.save_function_to_json('templates/test.json')
            print('配置文件保存成功！')
        except Exception as e:
            print('错误！保存文件出错！')

    def show_func(self, func):
        """对于载入的func进行前端显示"""
        self.cmb1.set(func.get_func_name())
        self.cmb2['values'] = func.get_procedure_names()

    def load_default_config(self, path='templates/data.json'):
        """载入数据"""
        try:
            self.func = self.ff.create_function_from_json(path)
            # 载入后设置前端显示
            self.show_func(self.func)

            print('读取配置文件成功！')
            print(self.func.get_data())
        except Exception as e:
            print('错误！读取配置文件出错！')

    def load_user_config(self):
        """载入用户数据"""
        file_path = askopenfilename()
        self.load_default_config(file_path)

    def pause(self):
        """暂停"""
        ...
        # TODO

    def write_dict(self):
        """将信息写入到dict中"""
        p_name = self.cmb2_value.get()
        if p_name != '':
            self.func.update(p_name, self.xy, self.color)
            print(self.func.get_data())

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

    def check_mouse_move(self):
        """检测鼠标移动，实时显示鼠标位置和颜色"""

        def check_mouse():
            while True:
                # 显示颜色设置
                tensix = self.get_postion_color()
                if tensix != '#-1-1-1':
                    self.e_color.configure(fg=tensix)
                    self.l_c.configure(fg=tensix)
                else:
                    self.e_color.configure(fg='red')
                sleep(self.settings.get_option('mouse', 'mouse_check_speed', 'float'))

        build_thread(check_mouse, '鼠标颜色检查')

    def func_start(self):
        """运行"""
        # 当前配置文件中的字典
        if self.func is not None:
            fr = FuncRun(self.func)
            fr.func_demo()
        else:
            print('错误！请创建流程，或者导入流程！')

    def destroy(self):
        self.root.quit()


if __name__ == '__main__':
    App().run()
