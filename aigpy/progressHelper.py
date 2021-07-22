#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   progressHelper.py
@Time    :   2018/12/28
@Author  :   Yaronzz 
@Version :   2.0
@Contact :   yaronhuang@foxmail.com
@Desc    :   Show ProgressBar
"""

import sys
import threading


class ProgressTool(object):
    def __init__(self, maxCount, barLength=50, icon='▓', unit='', desc=''):
        self.curCount = 0  # 当前计数
        self.maxCount = maxCount  # 最大数量
        self.barLength = barLength  # 进度条长度
        self.icon = icon  # 进度符号
        self.mutex = threading.Lock()  # 互斥锁
        self.isFinish = False
        self.unit = unit
        self.desc = ''
        if len(desc) > 0:
            self.desc = '(' + desc + ')'

    def reset(self, maxCount):
        if self.mutex.acquire():
            self.curCount = 0
            self.maxCount = maxCount
            self.isFinish = False
            self.mutex.release()

    def setCurCount(self, curCount):
        if self.mutex.acquire():
            if self.isFinish is False:
                if curCount >= self.maxCount:
                    curCount = self.maxCount
                    self.isFinish = True
                self.curCount = curCount
                self.__show__()
            self.mutex.release()

    def addCurCount(self, addCount):
        count = self.curCount + addCount
        self.setCurCount(count)

    def step(self):
        count = self.curCount + 1
        self.setCurCount(count)

    def __show__(self):
        try:
            # 计算显示几个进度块
            numBlock = int(self.curCount * self.barLength / self.maxCount)  # 计算显示多少个'>'
            # 计算显示几个空格
            numEmpty = self.barLength - numBlock
            # 计算百分比
            percent = self.curCount * 100.0 / self.maxCount
            # 输出字符串
            process = '%3d' % percent + '%|'
            process += self.icon * numBlock + ' ' * numEmpty + '| '
            process += str(round(self.curCount, 2)) + '/'
            process += str(round(self.maxCount, 2)) + ' ' + self.unit + self.desc

            # 判断是否要换行
            process += '\r' if self.curCount < self.maxCount else '\n'

            sys.stdout.write(process)
            sys.stdout.flush()
        except:
            pass
