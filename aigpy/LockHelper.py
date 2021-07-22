#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  LockHelper.py
@Date    :  2020/11/16
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :  
"""

import threading


class RWLock(object):
    def __init__(self):
        self.rlock = threading.Lock()
        self.wlock = threading.Lock()
        self.reader = 0

    def write_acquire(self):
        self.wlock.acquire()

    def write_release(self):
        self.wlock.release()

    def read_acquire(self):
        self.rlock.acquire()
        self.reader += 1
        if self.reader == 1:
            self.wlock.acquire()
        self.rlock.release()

    def read_release(self):
        self.rlock.acquire()
        self.reader -= 1
        if self.reader == 0:
            self.wlock.release()
        self.rlock.release()
