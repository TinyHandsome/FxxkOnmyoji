#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf-8 

"""
@author: Li Tian
@contact: litian_cup@163.com
@software: pycharm
@file: run_function.py
@time: 2021/2/4 15:16
@desc: 运行功能
"""

from dataclasses import dataclass
import time
from structure.function import Function
from structure.function_factory import FunctionFactory
from structure.row_factory import RowFactory
from structure.step import Step
from structure.point import Point
from supports.mk_factory import MKFactory
from supports.thread_management import ThreadManagement
from supports.info_pip import InfoPip
from supports.tip_time import TickTime


@dataclass
class RunStep:
    """运行步骤"""
    step: Step
    info_stack: InfoPip
    tt: TickTime
    row_fac: RowFactory
    func: Function

    # 超时检查的开关
    overtime_check: bool

    def __post_init__(self):
        self.location_points = self.step.get_location_points()
        self.click_points = self.step.get_click_points(p_type='c')
        self.multi_click_points = self.step.get_click_points(p_type='m')
        try:
            self.press_release_points = [self.step.get_click_points(p_type='p')[0],
                                         self.step.get_click_points(p_type='r')[0]]
        except:
            self.press_release_points = []
        self.pause_points = self.step.get_click_points(p_type='pause')

        # 鼠标键盘工厂
        self.mkf = MKFactory()

    def get_location_result(self):
        """检查当前各个location点位的检查情况"""
        location_result = [self.check_point_color(p) for p in self.location_points]
        return sum(location_result) == len(location_result)

    def run_step(self):
        """识别并点击"""
        if self.get_location_result():
            # 检查是否超时： [是否超时 and 超时检查是否打开 and 该step需要检查]
            if self.tt.update_time_and_check(self.step.step_name) and self.overtime_check and self.step.is_step_check():
                # 超时返回的是True，自己暂停
                return True
            else:
                # 没超时，开始狂点模式
                # 1. 识别场景后点击，此时更新text
                self.row_fac.flush_run_step(self.step.step_name)
                # 2. 点击每一个需要click的点
                self.click_all_points()
                # 3. 点玩后，初始化text
                self.row_fac.flush(self.func)

        else:
            # 没有检查到颜色，就暂停会儿叭
            ...

    def check_point_color(self, point: Point):
        """【v0.3 需要根据l和n进行判断和返回】检查一个点的颜色是否为True"""
        xy, color = point.get_loc_color()
        p_type, p_times = point.get_type_click_time()
        color_check_result = self.mkf.colorCheck(color, xy)

        try:
            assert isinstance(color_check_result, bool)
            if 'l' in p_type:
                # l的话，该返回啥返回啥
                return color_check_result
            elif 'n' in p_type:
                # n的话，返回反过来的值
                return not color_check_result
            else:
                # 讲道理这种情况是不会出现的，可万一呢
                self.info_stack.info('狗贼！快联系管理员！', 2)
                return False
        except Exception as e:
            # 如果颜色不是bool的话，那么color_check_result就是结果和颜色
            self.info_stack.info(*color_check_result)
            return False

    def click_all_points(self):
        """【v0.32 检查后需要执行一切操作】点击所有需要点击的点"""
        # 点击c
        for p in self.click_points:
            self.run_click_point(p)
        # 点击m
        self.run_multi_click_points(self.multi_click_points)
        # 进行拖拽
        try:
            self.run_press_release_points(self.press_release_points[0], self.press_release_points[1])
        except:
            ...
        # 暂停：多个暂停点，一个step只取最后的时间
        try:
            self.run_pause_points(self.pause_points[-1])
        except:
            ...

    def run_click_point(self, point: Point):
        """点击"""
        xy, color = point.get_loc_color()
        if point.click_times == '0':
            # 讲道理，这种情况是不会有的，万一有憨批呢，对吧
            ...
        elif point.click_times == '1':
            # 点击一次
            self.mkf.l1(xy)
        else:
            # 点击多次
            self.mkf.ln(xy)

    def run_multi_click_points(self, points: [Point]):
        """运行顺序点击"""
        m_point_dict = {}
        for m_point in points:
            m_point_dict[m_point.get_m_order()] = m_point

        sorted_points = [y[1] for y in sorted(m_point_dict.items(), key=lambda x: x[0], reverse=True)]
        for p in sorted_points:
            self.run_click_point(p)

    def run_press_release_points(self, point_p: Point, point_r: Point):
        """运行拖拽点"""
        self.mkf.l_pr(point_p.get_loc(), point_r.get_loc())

    def run_pause_points(self, point: Point):
        """暂停点"""
        time.sleep(point.get_click_time())


@dataclass
class RunFunction:
    func: Function
    ff: FunctionFactory
    tm: ThreadManagement
    info_stack: InfoPip
    row_fac: RowFactory

    # 超时检查的开关
    overtime_check: bool

    def __post_init__(self):
        # 时间管理大师，管理功能的所有步骤，如果某一个步骤在短时间内点击多次，则暂停
        self.tt = TickTime()

    '''弃用
    def run_step(self, step: Step):
        """运行一个步骤"""
        # 【检查step中点的颜色】获取每个点的检查结果，如果标记带l的都是True则执行标记带c的点
        location_result = [self.check_point_color(p) for p in step.get_location_points()]

        # 【颜色都对，则运行有loc和color值的点】如果检查的结果都为True，则识别该流程被触发，执行点击事件
        if sum(location_result) == len(location_result):
            c_points = step.get_click_points()

            # 这里可能没有点信息
            if not c_points:
                # 【v0.3】这里应该不会执行，因为在[check_before_run]函数中已经进行了判断
                self.info_stack.info('步骤：' + step.step_name + '无效...', 2)
            else:
                # 时间检查，是否超时
                if self.tt.update_time_and_check(step.step_name):
                    # 超时返回的是True，结束叭，设置结束，并自己结束
                    self.info_stack.info('脚本检测超时，自动暂停所有功能', 2)
                    self.pause(shown_info=False)

                # 点击每一个需要click的点
                for cp in c_points:
                    self.click_point(cp)

        else:
            # 都不是True能怎么办，啥都不干呗
            ...

        # 监听频率
        self.t.tip('color')
    '''

    def run_step(self, step: Step):
        """运行一个步骤"""
        rs = RunStep(step, self.info_stack, self.tt, self.row_fac, self.func, self.overtime_check)
        need_pause = rs.run_step()
        if need_pause:
            self.info_stack.info('脚本检测超时，自动暂停所有功能', 2)
            self.tm.pause(self.func.func_name, shown_info=False)

    def run_function(self):
        """运行一个功能，包括多个步骤"""
        # 获取该功能的所有步骤和connections的所有步骤
        for s in self.ff.get_effective_steps(self.func):
            self.tm.build_thread(self.run_step, s.step_name, is_while=True, args=(s,))
