#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   systemHelper.py
@Time    :   2018/12/20
@Author  :   Yaron Huang 
@Version :   1.0
@Contact :   yaronhuang@qq.com
@Desc    :   
'''
import os
import platform

def getOwnPath(in__file__):
    return os.path.dirname(os.path.realpath(in__file__))

def isWindows():
    sysName = platform.system()
    return sysName == "Windows"

def isLinux():
    sysName = platform.system()
    return sysName == "Linux"
