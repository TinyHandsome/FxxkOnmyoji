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
        4. [tk.Menu](https://blog.csdn.net/weixin_42272768/article/details/100809120)
        5. [tk设置窗口图表的三种方式](https://blog.csdn.net/nilvya/article/details/104822196/)
        6. [pyinstaller参数详解](http://c.biancheng.net/view/2690.html)
           [pyinstaller官方文档](https://pyinstaller.readthedocs.io/en/v4.2/usage.html)
           pyinstaller -D -w -y -n 平平无奇的阴阳师养成工具 -i ./configures/自由之翼.ico tk_app.pyw --distpath=C:/Users/liyingjun/Desktop/gouzei/dist --workpath=C:/Users/liyingjun/Desktop/gouzei/build --add-data="configures;configures"
           【弄完后记得删除configures/update_configs.ini】

"""
import webbrowser
from functools import partial
import os
from dataclasses import dataclass
from time import sleep
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename, askopenfilenames

from system_hotkey import SystemHotkey

from structure.function_factory import FunctionFactory
from structure.run_function import RunFunction
from structure.row_factory import RowFactory
from supports.configure_tools import Configure
from supports.functions import get_files_names, check_filefolder_exist
from supports.info_pip import InfoPip
from supports.log_factory import LogFactory
from supports.mouse_action import MouseAction
from supports.update_configure_tools import UpdateConfigureTools
from supports.set_windows import SetWin
from supports.thread_management import ThreadManagement


@dataclass
class App:
    is_test: bool

    def __post_init__(self):

        self.init_area()
        self.init_global_var()
        self.init_tk()

    def init_global_var(self):
        """全局变量初始化"""

        # 初始坐标和颜色
        self.xy, self.color = '', ''
        # 初始化功能集合
        self.functions = None
        # 初始化当前选择的功能
        self.current_func = None
        # 初始化运行的功能
        self.rf = None
        # 载入文件的名字
        self.load_file_name_without_suffix = None

    def init_tk(self):
        """初始化tk"""

        """读取各种配置"""
        frame_label_pad = self.settings.get_option('gui', 'frame_label_pad', 'int')
        label_width = self.settings.get_option('gui', 'label_width', 'int')
        label_ipadx = self.settings.get_option('gui', 'label_ipadx', 'int')
        button_width = self.settings.get_option('gui', 'button_width', 'int')
        button_ipadx = self.settings.get_option('gui', 'button_ipadx', 'int')
        cmb1_width = self.settings.get_option('gui', 'cmb1_width', 'int')
        cmb2_width = self.settings.get_option('gui', 'cmb2_width', 'int')
        e_xy_length = self.settings.get_option('gui', 'e_xy_length', 'int')
        e_color_length = self.settings.get_option('gui', 'e_color_length', 'int')
        windows_width_input = self.settings.get_option('gui', 'windows_width_input', 'int')
        block_color = self.settings.get_option('gui', 'block_color')

        default_windows_width = self.settings.get_option('windows', 'default_width')

        """设置各种字体"""
        # 标题字体的大小
        font_type = self.settings.get_option('font', 'font_type')
        font_combobox = (
            font_type,
            self.settings.get_option('font', 'font_size_combobox', 'int'))
        # 文字字体大小
        font_normal = (
            font_type,
            self.settings.get_option('font', 'font_size_normal', 'int'))
        # frame字体大小
        font_labelframe = (
            font_type,
            self.settings.get_option('font', 'font_size_label', 'int'))
        # log字体大小
        font_labelLog = (
            font_type,
            self.settings.get_option('font', 'font_size_log', 'int'))
        font_labelCurrentLog = (
            font_type,
            self.settings.get_option('font', 'font_size_current_log', 'int'))
        font_me = (
            font_type,
            self.settings.get_option('font', 'font_size_bottom', 'int'))
        font_text = (
            font_type,
            self.settings.get_option('font', 'font_size_text', 'int')
        )

        """底层root初始化"""
        self.root = Tk()
        # 第一参数False 表示该图标图像仅适用于该特定窗口，而不适用于将来创建的 toplevels 窗口；
        # 如果设置为True ，则图标图像也将应用于以后创建的所有 toplevels 图像
        # self.root.iconphoto(True, PhotoImage(file='./configures/自由之翼.png'))
        self.root.iconbitmap('./configures/自由之翼.ico')
        self.root.title('平平无奇的阴阳师养成工具 v0.33')
        # 设置界面大小和位置
        self.root.geometry("+1200+200")
        # 设置关闭按钮的功能
        self.root.protocol('WM_DELETE_WINDOW', self.destroy)
        # 允许缩放的范围
        self.root.resizable(1, 0)

        """菜单栏"""
        self.menubar = Menu(self.root)
        self.file_menu = Menu(self.menubar, tearoff=0)
        self.setting_menu = Menu(self.menubar, tearoff=0)

        # 菜单
        self.menubar.add_cascade(label='菜单', menu=self.file_menu)
        self.cb_var_whether_top = BooleanVar()
        self.file_menu.add_checkbutton(label='置顶', variable=self.cb_var_whether_top,
                                       onvalue=True, offvalue=False,
                                       command=self.set_top_window)
        self.file_menu.add_command(label='调整界面(d)', command=self.set_two_win_left)
        self.file_menu.add_separator()
        # 初始化是否置顶
        self.cb_var_whether_top.set(True)

        self.file_menu.add_command(label='计时关闭（未完成）', command=...)
        self.file_menu.add_command(label='次数限制（未完成）', command=...)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='退出(c)', command=self.destroy)

        # 配置
        self.menubar.add_cascade(label='设置', menu=self.setting_menu)
        setting_menu_partial = partial(self.setting_menu.add_command, hidemargin=False)

        setting_menu_partial(label='载入默认配置(l)', command=self.load_default_config)
        setting_menu_partial(label='选择用户配置(L)', command=self.load_user_config)
        setting_menu_partial(label='重载功能(k)', command=self.update_functions)
        self.setting_menu.add_separator()
        setting_menu_partial(label='存为默认配置(s)', command=self.save_config_as_default)
        setting_menu_partial(label='存为其他文件(S)', command=self.save_config_to_file)
        self.setting_menu.add_separator()
        setting_menu_partial(label='单项融合(n)', command=self.combine_single_load)
        setting_menu_partial(label='多项融合(N)', command=self.combine_multiple_load)
        setting_menu_partial(label='自动融合(A)', command=self.combine_auto_load)

        # 用户手册
        self.menubar.add_command(label='用户手册', command=lambda: self.uct.show_my_words_at_first_open(True))

        self.root.config(menu=self.menubar)

        """frame_right_右边的text框"""
        self.frame_text = LabelFrame(self.root, text='| 自由之翼 |',
                                     labelanchor=N, font=font_labelframe,
                                     padx=frame_label_pad,
                                     pady=frame_label_pad, fg=block_color)

        self.procedure_text = Text(self.frame_text, width=16, height=2, font=font_text, wrap='none')
        self.procedure_text.pack(side=TOP, fill=BOTH, expand=True)

        self.frame_text.pack(side=RIGHT, fill=BOTH, anchor=N, padx=frame_label_pad, pady=frame_label_pad,
                             expand=True)

        """frame1_外框，功能、运行、暂停、退出、调整界面"""
        self.frame_1 = LabelFrame(self.root, text='| 海的那边 |',
                                  labelanchor=N, font=font_labelframe,
                                  padx=frame_label_pad,
                                  pady=frame_label_pad, fg=block_color)
        self.f11 = Frame(self.frame_1)

        self.cmb1_value = StringVar()
        self.cmb2_value = StringVar()

        self.l1 = Label(self.f11, text='功能', font=font_normal, justify='left', width=label_width)
        self.l1.pack(side=LEFT, fill=Y)
        self.cmb1 = ttk.Combobox(self.f11, textvariable=self.cmb1_value,
                                 width=cmb1_width, font=font_normal)
        # 初始化功能名字，从ini文件中获取
        self.functions = self.ff.init_functions_from_config()
        self.cmb1['values'] = self.ff.get_function_names()
        # 选择第一个为默认
        # self.cmb1.current(0)
        self.cmb1.bind('<<ComboboxSelected>>', self.get_cmb2_list_from_cmb1)
        self.cmb1.pack(side=LEFT, fill=BOTH, ipadx=button_ipadx, expand=True)
        self.b2 = Button(self.f11, text='运行(r)', command=self.func_start, font=font_normal, width=button_width)
        self.b2.pack(side=LEFT, fill=Y, ipadx=button_ipadx)

        self.f12 = Frame(self.frame_1)
        self.l_point = Label(self.f12, text='点位', font=font_normal, justify='left', width=label_width)
        self.l_point.pack(side=LEFT, fill=Y)
        self.cmb2 = ttk.Combobox(self.f12, textvariable=self.cmb2_value,
                                 width=cmb2_width, font=font_normal)
        self.cmb2.bind('<<ComboboxSelected>>', self.get_key)
        self.cmb2.pack(side=LEFT, fill=BOTH, ipadx=button_ipadx, expand=True)
        self.b4 = Button(self.f12, text='暂停/继续(p)', command=self.pause, font=font_normal, width=button_width)
        self.b4.pack(side=LEFT, fill=Y, ipadx=button_ipadx)

        """调整界面
        self.l_adjust = Label(self.f12, text='定宽', font=font_normal)
        self.l_adjust.pack(side=LEFT, fill=Y, ipadx=label_ipadx)
        # 宽度取值
        self.reset_windows_width = StringVar()
        self.e_width = Entry(self.f12, width=windows_width_input,
                             textvariable=self.reset_windows_width, font=font_normal, justify='center')
        self.e_width.insert(END, default_windows_width)
        self.e_width.pack(side=LEFT, fill=Y)
        self.b_adjust_win = Button(self.f12, text='调整界面(d)', font=font_normal,
                                   command=self.set_two_win_left)
        self.b_adjust_win.pack(side=LEFT, fill=Y, ipadx=button_ipadx)
        """

        self.f13 = Frame(self.frame_1)
        self.xy_value = StringVar()
        self.color_value = StringVar()
        self.l_c = Label(self.f13, text='坐标', font=font_normal, justify='left', width=label_width)
        self.l_c.pack(side=LEFT, fill=Y)
        self.e_xy = Entry(self.f13, width=e_xy_length,
                          textvariable=self.xy_value, font=font_normal, justify='center')
        self.e_xy.insert(END, self.xy)
        self.e_xy.pack(side=LEFT, fill=Y)
        self.e_color = Entry(self.f13, width=e_color_length,
                             textvariable=self.color_value, font=font_normal, justify='center')
        self.e_color.insert(END, self.color)
        self.e_color.pack(side=LEFT, fill=BOTH, expand=True)
        self.b1 = Button(self.f13, text='写入(w)', command=self.write_info, font=font_normal, width=button_width)
        self.b1.pack(side=LEFT, fill=Y)

        """置顶、用户手册、载入配置、退出
        # self.cb_var_whether_top = BooleanVar()
        # self.cb1 = Checkbutton(self.f12, text='置顶', variable=self.cb_var_whether_top,
        #                        font=font_normal, onvalue=True, offvalue=False,
        #                        command=self.set_top_window,
        #                        justify='left',
        #                        )
        # # 初始化是否置顶
        # self.cb_var_whether_top.set(True)
        # self.cb1.pack(side=LEFT, fill=Y, ipadx=label_ipadx)
        # self.b6 = Button(self.f12, text='用户手册', command=lambda: self.uct.show_my_words_at_first_open(True),
        #                  font=font_normal, bg='lightblue')
        # self.b6.pack(side=LEFT, fill=BOTH, ipadx=button_ipadx, expand=YES)
        # self.b4 = Button(self.f12, text='载入默认配置(l)', command=self.load_default_config, font=font_normal)
        # self.b4.pack(side=LEFT, fill=Y, ipadx=button_ipadx)
        # self.b5 = Button(self.f12, text='选择用户配置(L)', command=self.load_user_config, font=font_normal)
        # self.b5.pack(side=LEFT, fill=Y, ipadx=button_ipadx)
        # self.b3 = Button(self.f12, text='退出(c)', command=self.destroy, font=font_normal, width=6)
        # self.b3.pack(side=LEFT, fill=Y, ipadx=button_ipadx)
        """

        self.f11.pack(fill=BOTH)
        self.f12.pack(fill=BOTH)
        self.f13.pack(fill=BOTH)

        """
        frame2外框_各种坐标处理
        self.frame_2 = LabelFrame(self.root, text='| 坐标之力 |', labelanchor=N, font=font_labelframe, padx=frame_label_pad,
                                  pady=frame_label_pad, fg=block_color)
        self.f21 = Frame(self.frame_2)

        # 两个entry的值
        self.xy_value = StringVar()
        self.color_value = StringVar()

        self.l_c = Label(self.f21, text='坐标颜色', font=font_normal)
        self.l_c.grid(row=0, column=0)

        self.e_xy = Entry(self.f21, width=e_xy_length,
                          textvariable=self.xy_value, font=font_normal, justify='center')
        self.e_xy.insert(END, self.xy)
        self.e_xy.grid(row=0, column=1, sticky='nesw')

        self.e_color = Entry(self.f21, width=e_color_length,
                             textvariable=self.color_value, font=font_normal, justify='center')
        self.e_color.insert(END, self.color)
        self.e_color.grid(row=0, column=2, columnspan=2, sticky='nesw')

        self.l_conf = Label(self.f21, text='保存配置', font=font_normal)
        self.l_conf.grid(row=1, column=0)

        self.b1 = Button(self.f21, text='写入坐标(w)', command=self.write_info, font=font_normal)
        self.b1.grid(row=1, column=1, sticky='nesw')
        self.b_save_conf = Button(self.f21, text='存为默认(s)', font=font_normal,
                                  command=self.save_config_as_default)
        self.b_save_conf.grid(row=1, column=2, sticky='nesw')
        self.b_save_to_file = Button(self.f21, text='存到文件(S)', font=font_normal,
                                     command=self.save_config_to_file)
        self.b_save_to_file.grid(row=1, column=3, sticky='nesw')

        self.l_combine = Label(self.f21, text='合并配置', font=font_normal)
        self.l_combine.grid(row=2, column=0)
        self.b_single_combine = Button(self.f21, text='单项融合(n)', command=self.combine_single_load, font=font_normal)
        self.b_single_combine.grid(row=2, column=1, sticky='nesw')
        self.b_multiple_combine = Button(self.f21, text='多项融合(N)', command=self.combine_multiple_load, font=font_normal)
        self.b_multiple_combine.grid(row=2, column=2, sticky='nesw')
        self.b_auto_combine = Button(self.f21, text='自动融合(A)', command=self.combine_auto_load, font=font_normal)
        self.b_auto_combine.grid(row=2, column=3, sticky='nesw')

        self.f21.pack(fill=BOTH)
        """

        """frame3 待开发"""
        self.frame_3 = LabelFrame(self.root, text='| 献出心脏 |', labelanchor=N,
                                  font=font_labelframe,
                                  padx=frame_label_pad,
                                  pady=frame_label_pad,
                                  fg=block_color)
        self.f31 = Frame(self.frame_3)

        self.current_info = StringVar()
        self.l_first = Label(self.f31, textvariable=self.current_info,
                             justify=LEFT, font=font_labelCurrentLog,
                             # height=1,
                             )
        self.l_first.pack(anchor=N, side=TOP)

        self.history_info = StringVar()
        self.l_history = Label(self.f31,
                               textvariable=self.history_info,
                               # wraplength=200,
                               justify=LEFT,
                               font=font_labelLog,
                               fg='grey',
                               height=2
                               )
        self.l_history.pack(anchor=N, side=TOP)

        # self.l_me = Label(self.f31, text='作者：李英俊小朋友', justify=RIGHT)
        # self.l_me.pack(anchor=SE, side=BOTTOM)

        self.f31.pack(side=TOP, fill=BOTH, expand=True)

        """布局"""
        # padx、pady是框架外部距离框架的距离
        self.frame_1.pack(side=TOP, fill=X, anchor=N, padx=frame_label_pad, pady=frame_label_pad, expand=True)
        # self.frame_2.pack(side=LEFT, fill=None, anchor=NW, padx=frame_label_pad, pady=frame_label_pad)
        self.frame_3.pack(side=TOP, fill=BOTH, anchor=N, padx=frame_label_pad, pady=frame_label_pad,
                          expand=True)

        """版权信息"""
        self.l_bottom1 = Label(text='仅供学习交流使用，禁止用于任何商业用途！', justify='left',
                               font=font_me, fg='grey')
        self.l_bottom1.pack(side=LEFT)
        self.l_bottom1.bind("<Button-1>", lambda e: (
            webbrowser.open("https://github.com/TinyHandsome"),
            self.root.title('点了我的github你就是我的人了吼吼~')
        ))
        self.l_bottom2 = Label(text='@李英俊小朋友', justify='right', font=font_me, fg='grey')
        self.l_bottom2.pack(side=RIGHT)
        self.l_bottom2.bind("<Button-1>", lambda e: (
            webbrowser.open("https://blog.csdn.net/qq_21579045"),
            self.root.title('点了我的CSDN你就是我的人了嘻嘻~')
        ))

        """各个跟tk组件有关的工具"""
        # 信息输出栈
        self.info_stack = InfoPip(self.current_info, self.history_info, self.l_first, self.log_factory)
        # 线程管理
        self.tm = ThreadManagement(self.info_stack)
        # 行处理
        self.row_factory = RowFactory(self.procedure_text)

    def init_area(self):
        """初始化区域"""
        # 全局快捷键设置
        self.hk = SystemHotkey()
        # 移动鼠标
        self.ma = MouseAction()
        # 配置初始化
        self.settings = Configure('configures/configs.ini')
        # 设置阴阳师界面位置
        self.sw = SetWin()
        # 操作功能配置文件的工具
        self.ff = FunctionFactory()
        # 其他效果管理
        self.uct = UpdateConfigureTools(is_test=self.is_test)
        # 日志管理
        self.log_factory = LogFactory()

    def hotKey_bind(self):
        """全局快捷键设置"""
        # 设置偏函数，这里实现已有映射的覆盖
        partial_register = partial(self.hk.register, overwrite=True)

        partial_register(('alt', 'w'), callback=lambda e: self.write_info())
        partial_register(('alt', 'c'), callback=lambda e: self.destroy())
        partial_register(('alt', 'r'), callback=lambda e: self.func_start())
        partial_register(('alt', 'p'), callback=lambda e: self.pause())
        partial_register(('alt', 's'), callback=lambda e: self.save_config_as_default())
        partial_register(('alt', 'shift', 's'), callback=lambda e: self.save_config_to_file())
        partial_register(('alt', 'l'), callback=lambda e: self.load_default_config())
        partial_register(('alt', 'shift', 'l'), callback=lambda e: self.load_user_config())
        partial_register(('alt', 'k'), callback=lambda e: self.update_functions())
        partial_register(('alt', 'n'), callback=lambda e: self.combine_single_load())
        partial_register(('alt', 'shift', 'n'), callback=lambda e: self.combine_multiple_load())
        partial_register(('alt', 'shift', 'a'), callback=lambda e: self.combine_auto_load())
        partial_register(('alt', 'd'), callback=lambda e: self.set_two_win_left())

    def clear_logs(self):
        """清除7天前的日志数据"""
        keep_days = self.settings.get_option('logs', 'keep_days', 'int')
        clear_count = self.log_factory.clear_logs(keep_days)
        if clear_count != 0:
            self.info_stack.info('删除了【' + str(clear_count) + '】个日志文件...', 3)

    def set_top_window(self, shown_info=True):
        """设置是否置顶"""
        if self.cb_var_whether_top.get():
            if shown_info:
                self.info_stack.info('设置软件置顶', 1)
            self.root.wm_attributes('-topmost', 1)
        else:
            if shown_info:
                self.info_stack.info('取消软件置顶', 1)
            self.root.wm_attributes('-topmost', 0)

    def set_two_win_left(self, is_print=True):
        """设置两个阴阳师的界面排在左边"""
        self.win_settings = self.settings.get_items('windows')
        handles = self.sw.find_onmyoji_handle()
        if handles[0] == 0:
            self.info_stack.info('未打开阴阳师！', 2)
            return

        # 遍历阴阳师所有句柄
        count = 0
        for h in range(len(handles)):
            count += 1
            # 提取第h个坐标，h只有1的话，就只提取一个坐标
            # 这里h+1的原因是，第一个参数是默认宽度，不是win_loc
            loc = [int(temp) for temp in self.win_settings[h + 1][1].split(',')]
            # 按照输入的最新宽度设置界面宽度
            # repair_width = int(self.reset_windows_width.get())
            repair_width = self.settings.get_option('windows', 'default_width', 'int')
            if repair_width != '':
                loc[-1] = repair_width
                # 如果输入了数值，则按数值来重设宽度
                if count == 1:
                    # 第一个界面，123不动，调整4
                    ...
                elif count == 2:
                    # 第二个界面，13不动，调整24
                    win2_locked_2 = self.settings.get_option('windows', 'win2_locked_2', 'int')
                    if win2_locked_2 == -1:
                        loc[1] = repair_width - 8
                    else:
                        loc[1] = win2_locked_2
                elif count == 3:
                    # 第三个界面，右上，23不动，调整14
                    win3_locked_1 = self.settings.get_option('windows', 'win3_locked_1', 'int')
                    if win3_locked_1 == -1:
                        loc[0] = repair_width + 280
                    else:
                        loc[0] = win3_locked_1
                else:
                    self.info_stack.info('你有病不是？你打开这么多阴阳师干嘛啊', 2)

            try:
                self.sw.move_rect(handles[h], loc)
            except Exception as e:
                self.info_stack.info('调整界面失败', 2)
                return
        if is_print:
            self.info_stack.info('调整界面', 3)

    def run(self):
        """启动，预备设置"""

        """其他线程建立"""
        # 检查鼠标颜色
        self.tm.build_thread(self.check_mouse_move, '_鼠标颜色检查')
        # 检测是否打开notification
        self.tm.build_thread(self.uct.show_my_words_at_first_open, '_打开notification', is_while=False)

        """其他功能实现"""
        # 全局快捷键设置
        self.hotKey_bind()
        # 清除过期的log
        self.clear_logs()
        # 检查templates文件是否存在
        check_filefolder_exist('templates')
        # 执行置顶的默认
        self.set_top_window(shown_info=False)

        """界面循环"""
        # 开始循环
        self.root.mainloop()

    def get_cmb2_list_from_cmb1(self, is_shown=True, *args):
        """cmb1对应的函数，获取对应下拉框的list，方便写入后续下拉框"""
        cmb1_v = self.cmb1_value.get()
        if is_shown:
            self.info_stack.info(cmb1_v, 1)
        # 当前功能为
        self.current_func = self.ff.get_function_from_function_name(cmb1_v)
        # 设置下拉框的值
        self.cmb2['values'] = self.current_func.get_point_names()
        # 清空下拉框
        self.cmb2_value.set('')

        # 刷新text数据
        self.row_factory.flush(self.current_func)

    def get_key(self, *args):
        """cmb2的对应的函数"""
        cmb2_v = self.cmb2_value.get()
        self.info_stack.info(cmb2_v, 1)

    def save_config_as_default(self):
        """保存当前设置"""
        try:
            self.ff.save_functions2json(self.functions, 'templates/默认保存文件.json')
            self.info_stack.info('配置文件保存成功', 3)
        except Exception as e:
            self.info_stack.info('保存文件出错', 2)

    def save_config_to_file(self):
        try:
            file_path = asksaveasfilename(defaultextension='.json', filetypes=[("Json文件", ".json")], initialdir='dir',
                                          title='Save as')
            self.ff.save_functions2json(self.functions, file_path)
            self.info_stack.info('配置文件保存成功', 3)
        except Exception as e:
            # print(repr(e))
            self.info_stack.info('保存文件出错！', 2)

    def set_last_open_funcname(self, load_file_name):
        """
        导入后，设置当前的功能名
            1. 注意：只有show_info为True才设置，因为融合，不设置
        """
        last_func_name = self.uct.get_last_open_funcname(load_file_name)
        current_func_names = self.cmb1['values']

        # 如果功能名不在当前功能名list中，则设置为第一个
        if last_func_name not in current_func_names:
            self.cmb1.current(0)
        else:
            self.cmb1_value.set(last_func_name)

        # 设置当前的func为所选功能
        self.get_cmb2_list_from_cmb1(is_shown=False)

    def load_default_config(self, path='templates/默认保存文件.json', show_info=True):
        """载入数据"""
        self.load_file_name_without_suffix = get_files_names(path)
        try:
            # 从json中创建数据，同时会获取初始化function_dict
            self.functions = self.ff.load_functions_from_json(path)
            # 载入后设置前端显示
            if show_info:
                self.info_stack.info('读取配置文件成功', 3)
            # 载入数据后，需要将两个值置为空
            self.cmb1_value.set('')
            self.cmb2_value.set('')

            self.cmb1['values'] = self.ff.get_function_names()

            # 载入后设置funcname
            self.set_last_open_funcname(self.load_file_name_without_suffix)

            return self.functions

        except Exception as e:
            self.info_stack.info('读取失败：' + str(e), 2)
            return None

    def load_user_config(self, show_info=True):
        """载入用户数据"""
        file_path = askopenfilename()
        # 如果中途返回了，就当无事发生
        if file_path == '':
            return ''

        self.load_default_config(file_path, show_info)
        return file_path

    def rebuild_function_factory(self):
        """根据最新的functions，重建function_factory，并更新下拉框"""
        # 重建function_factory
        self.ff.create_functions_dict(self.functions)
        # 更新下拉框
        self.cmb1['values'] = self.ff.get_function_names()
        # 重选最新功能
        self.get_cmb2_list_from_cmb1(False)

    def combine_single_load(self):
        """
        【单项融合】区别于多项融合，基于当前配置的（当前也可以是初始化配置）
            1. 开始需要导入一个json文件
            2. 如果未导入，则使用默认初始化json，则该导入基本就无效了
            3. 用导入的json填充当前json（遵守，点数量原则）
        """
        result_functions = self.functions
        # 载入选择的配置作为融合配置，原来的配置作为基础融合配置
        file_path = self.load_user_config(show_info=False)

        # 如果中途返回了，就当无事发生
        if file_path == '':
            return ''

        file_name_without_suffix = get_files_names(file_path)

        for f in self.functions:
            result_functions = self.ff.set_functions_by_step(result_functions, f)

        # 手动更新functions，并重建字典和下拉框
        self.functions = result_functions
        self.rebuild_function_factory()

        # 输出信息
        self.info_stack.info('<' + file_name_without_suffix + '>已融合进当前功能集中', 3)

    def update_functions(self):
        """
        【重载功能】更新当前functions中所有的数据
        场景：
            1. 当前功能写入几个点
            2. 更新了functions.ini的步骤
            3. 想要在当前的基础上，加入新建的步骤，并且保存已有的点位信息
        方法：
            1. 获取初始化功能functions
            2. 利用single融合的原理，传入初始化到当前中
        """
        result_functions = self.ff.init_functions_from_config()
        for f in self.functions:
            result_functions = self.ff.set_functions_by_step(result_functions, f)

        # 手动更新functions，并重建字典和下拉框
        self.functions = result_functions
        self.rebuild_function_factory()

        # 输出信息
        self.info_stack.info('所有功能和步骤已更到最新', 3)

    def combine_multiple_load(self, auto_file_paths=None):
        """
        【多项融合】融合载入用户数据，基于初始化配置的
            1. 基于基础functions.ini
            2. 将所选json，融合到functions.ini，无序操作
            3. 适用于，多个功能没有交叉使用的，
            4. 不适用于，功能优化，比如以前的点标错了，在其他功能更新了
            5. 建议保留原始json
        """
        if auto_file_paths is not None:
            # 自动的话，选取templates目录下所有的.json文件
            file_paths = auto_file_paths
        else:
            # 选取配置文件，并导入到self.functions
            file_paths = askopenfilenames()

        # 如果中途返回了，则当无事发生
        if file_paths == '':
            return ''

        # 编辑获取成功后的输出
        file_name_without_suffix = get_files_names(file_paths)
        names = ['<' + fn + '>' for fn in file_name_without_suffix]
        file_name_without_suffix = '、'.join(names)

        # 获取多个functions
        functions_matrix = []
        for file_path in file_paths:
            functions = self.load_default_config(file_path, show_info=False)
            if functions is not None:
                functions_matrix.append(functions)
            else:
                self.info_stack.info('多项融合出错', 2)

        # 获取初始化的文件
        result_functions = self.ff.init_functions_from_config()

        for now_functions in functions_matrix:
            # 将文件合并
            for func in now_functions:
                # 遍历当前功能list，看每个func是否在result_func中有名字
                result_functions = self.ff.set_functions_by_step(result_functions, func)

        # 手动更新functions，并重建字典和下拉框
        self.functions = result_functions
        self.rebuild_function_factory()

        # 输出信息
        self.info_stack.info(file_name_without_suffix + '已融合进当前功能集中', 3)

    def combine_auto_load(self):
        """
        【自动融合】融合templates目录下的所有json文件
            1. 基于combine_multiple_load实现
            2. 融合时，自动识别templates目录下的所有.json结尾的文件
        """
        template_path = './templates'
        files = [os.path.join(template_path, file) for file in os.listdir(template_path) if file.endswith('.json')]
        if not files:
            # 如果文件夹中没有.json文件
            self.info_stack.info('你这里面啥也没有啊！', 2)
            return None

        self.combine_multiple_load(files)

    def pause(self):
        """暂停"""
        if self.rf is not None:
            self.tm.pause(self.current_func.func_name)
        else:
            self.info_stack.info('未运行任何功能', 2)

    def write_info(self):
        """将信息写入到dict中"""
        p_name = self.cmb2_value.get()
        if p_name != '':
            self.current_func.update_point(p_name, self.xy, self.color)
            self.info_stack.info('写入【' + p_name + '】的坐标', 3)

        # 刷新text
        self.row_factory.flush(self.current_func)

    def get_postion_color(self):
        """设置绑定后的按键操作的值"""

        def extend_color(color: tuple):
            """将rgb颜色转换为rgb_16进制"""
            ten_six = "#%02x%02x%02x" % (color[0], color[1], color[2])
            return str(color) + ' | ' + ten_six, ten_six

        # 将暂停检查逻辑从坐标改为颜色
        temp_color = self.color
        self.xy, self.color = self.ma.get_mouse_postion_color().get_info()

        if self.color != temp_color:
            self.e_xy.delete(0, END)
            self.e_xy.insert(END, str(self.xy))
            self.e_color.delete(0, END)
            insert_info, tensix = extend_color(self.color)
            self.e_color.insert(END, insert_info)
            return tensix

    def check_mouse_move(self):
        """检测鼠标移动，实时显示鼠标位置和颜色"""

        # 显示颜色设置
        tensix = self.get_postion_color()
        if tensix != '#-1-1-1':
            # 不改变entry的颜色
            # self.e_color.configure(fg=tensix)
            self.b1.config(fg=tensix)
        else:
            # self.e_color.configure(fg='red')
            ...
        sleep(self.settings.get_option('mouse', 'mouse_check_speed', 'float'))

    def check_before_run(self):
        """运行前的检查"""
        # 检查是否选择了功能
        if self.current_func is None:
            self.info_stack.info('没有选择功能', 2)
            return False
        # 检查功能中是否存在至少一个点是有效的
        if not self.current_func.check_effective():
            self.info_stack.info('<' + self.current_func.func_name + '>中所有点都无效', 2)
            return False
        # 检查功能的关联功能是否存在一个点是有效的
        for code in self.current_func.connections:
            temp_f = self.ff.function_dict_by_code.get(code)
            if temp_f is None:
                self.info_stack.info('未找到编号为' + code + '的功能', 2)
                return False
            if not temp_f.check_effective():
                self.info_stack.info('【关联】功能：' + code + '所有点无效', 2)
                return False

        return True

    def func_start(self):
        """运行"""
        # 检查是否能运行
        if not self.check_before_run():
            return

        self.info_stack.info(self.current_func.func_name + '启动...', 3)
        # 记录当前function_name作为最后运行功能
        self.uct.update_last_open_funcname(self.current_func, self.load_file_name_without_suffix)

        self.rf = RunFunction(self.current_func, self.ff, self.tm, self.info_stack, self.row_factory)
        self.rf.run_function()

    def destroy(self):
        self.root.quit()
        # 关闭日志文件
        self.log_factory.close_log_file()


if __name__ == '__main__':
    App(is_test=False).run()
