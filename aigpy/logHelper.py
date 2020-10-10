#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   logHelper.py
@Time    :   2019/02/28
@Author  :   Yaronzz 
@Version :   2.0
@Contact :   yaronhuang@foxmail.com
@Desc    :   LOG FILE TOOL
'''
import os
import time

def write(path, string):
    try:
        fd = open(path, 'a+')
        fd.write(string + '\n')
        fd.close()
        return True
    except:
        return False  

def writeByTime(path, string):
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return write(path, '[' + date + ']  ' + string)
 
 
def clear(path):
    try:
        os.remove(path)
    except:
        pass
