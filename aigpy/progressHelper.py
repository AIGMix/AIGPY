#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   progressHelper.py
@Time    :   2018/12/28
@Author  :   Yaronzz 
@Version :   2.0
@Contact :   yaronhuang@foxmail.com
@Desc    :   Show ProgressBar
'''

import sys
import time
import threading

class ProgressTool(object):
    def __init__(self, maxCount, barLength=50, icon='▓', unit='', desc=''):
        self.curCount  = 0                  #当前计数
        self.maxCount  = maxCount           #最大数量
        self.barLength = barLength          #进度条长度
        self.icon      = icon               #进度符号
        self.mutex     = threading.Lock()   #互斥锁
        self.end       = 0
        self.unit      = unit
        self.desc      = ''
        if len(desc) > 0:
            self.desc = '(' + desc + ')'

    def reset(self, maxCount):
        if self.mutex.acquire():
            self.curCount = 0  
            self.maxCount = maxCount  
            self.end      = 0
            self.mutex.release()

    def setCurCount(self, curCount):
        if self.mutex.acquire():
            if self.end == 0:
                if curCount >= self.maxCount:
                    curCount = self.maxCount
                    self.end = 1
                self.curCount = curCount
                self._show()
            self.mutex.release()
    
    def addCurCount(self, addCount):
        if self.mutex.acquire():
            if self.end == 0:
                if self.curCount + addCount >= self.maxCount:
                    self.curCount = self.maxCount
                    self.end = 1
                else:
                    self.curCount += addCount
                self._show()
            self.mutex.release()

    def step(self):
        if self.mutex.acquire():
            if self.end == 0 and self.curCount < self.maxCount:
                self.curCount += 1
                self._show()
            else:
                self.end = 1
            self.mutex.release()

    def _show(self):
        #计算显示几个进度块
        numBlock = int(self.curCount * self.barLength / self.maxCount)  # 计算显示多少个'>'
        #计算显示几个空格
        numEmpty = self.barLength - numBlock
        #计算百分比
        percent = self.curCount * 100.0 / self.maxCount  
        #输出字符串
        process = '%3d' % percent + '%|' + self.icon*numBlock + ' '*numEmpty + '| ' + \
            str(round(self.curCount, 2)) + '/' + \
            str(round(self.maxCount, 2)) + ' ' + self.unit + self.desc

        #判断是否要换行
        if self.curCount < self.maxCount:
            process += '\r'
        else:
            process += '\n'
            
        sys.stdout.write(process)  
        sys.stdout.flush()

