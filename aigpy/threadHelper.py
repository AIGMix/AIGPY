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
import sys
import threading

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from concurrent.futures import wait
from concurrent.futures import ALL_COMPLETED

class ThreadTool(object):
    def __init__(self, maxThreadNum):
        self.allTask = []
        self.thread  = ThreadPoolExecutor(max_workers=maxThreadNum)
        
    def start(self, function, *args, **kwargs):
        """启动线程"""
        if(len(args) > 0 and len(kwargs) > 0):
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
    
    def close(self):
        self.thread.shutdown(False)


class ThreadPoolManger(object):
    def __init__(self, maxThreadNum):
        v = sys.version_info
        if v[0] > 2:
            import queue
            self.work_queue = queue.Queue()
        else:
            import Queue
            self.work_queue = Queue.Queue()

        self.allTask    = []
        self.thread     = ThreadPoolExecutor(max_workers=maxThreadNum)
        for i in range(maxThreadNum):
            handle = self.thread.submit(self.__workThread__)
            self.allTask.append(handle)

    def __workThread__(self):
        while True:
            func, args = self.work_queue.get()
            func(*args)
            self.work_queue.task_done()

    def addWork(self, func, *args):
        self.work_queue.put((func, args))
    
    def close(self):
        self.thread.shutdown(False)

