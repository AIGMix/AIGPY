#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   threadHelper.py
@Time    :   2018/12/17
@Author  :   Yaronzz 
@Version :   2.0
@Contact :   yaronhuang@foxmail.com
@Desc    :   Thread Tool 
"""

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed


class ThreadTool(object):
    def __init__(self, maxThreadNum: int):
        self.allTask = []
        self.thread = ThreadPoolExecutor(max_workers=maxThreadNum)

    def start(self, function, *args, **kwargs):
        if len(args) > 0 and len(kwargs) > 0:
            handle = self.thread.submit(function, *args, **kwargs)
        elif len(args) > 0:
            handle = self.thread.submit(function, *args)
        elif len(kwargs) > 0:
            handle = self.thread.submit(function, **kwargs)
        else:
            handle = self.thread.submit(function)

        self.allTask.append(handle)
        return handle

    def isFinish(self, handle):
        return handle.done()

    def getResult(self, handle):
        return handle.result()

    def waitAll(self):
        array = []
        for future in as_completed(self.allTask):
            data = future.result()
            array.append(data)
        return array

    def waitAnyone(self):
        as_completed(self.allTask)

    def close(self):
        self.thread.shutdown(False)
