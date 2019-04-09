#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   threadHelper.py
@Time    :   2018/12/17
@Author  :   Yaron Huang 
@Version :   1.0
@Contact :   yaronhuang@qq.com
@Desc    :   Thread Tool 
'''

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from concurrent.futures import wait
from concurrent.futures import ALL_COMPLETED

class ThreadTool(object):
    def __init__(self, maxThreadNum):
        self.allTask = []
        self.thread = ThreadPoolExecutor(max_workers=maxThreadNum)

    def start(self, function, *args, **kwargs):
        """启动线程"""
        if(len(args) > 0 and len(kwargs) > 0):
            handle = self.thread.submit(function, *args, **kwargs)
        elif len(args) > 0:
            handle = self.thread.submit(function, *args)
        elif len(kwargs) > 0:
            handle = self.thread.submit(function, **kwargs)

        self.allTask.append(handle)
        return handle

    def isFinish(self, handle):
        """线程是否结束"""
        return handle.done()

    def getResult(self, handle):
        """获取线程结果"""
        return handle.result()

    def waitAll(self):
        """等待全部线程结束"""
        for future in as_completed(self.allTask):
            data = future.result()
        # wait(self.allTask, return_when=ALL_COMPLETED)

    def waitAnyone(self):
        """等待任何一个线程技术"""
        as_completed(self.allTask)

    
