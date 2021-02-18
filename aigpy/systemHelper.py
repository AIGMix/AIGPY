#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
@File    :   systemHelper.py
@Time    :   2018/12/20
@Author  :   Yaronzz 
@Version :   2.0
@Contact :   yaronhuang@foxmail.com
@Desc    :   
'''
import platform


def isWindows():
    sysName = platform.system()
    return sysName == "Windows"


def isLinux():
    sysName = platform.system()
    return sysName == "Linux"


def cmpVersion(ver1: str, ver2: str):
    array1 = ver1.split('.')
    array2 = ver2.split('.')
    iIndex = 0
    for obj in array1:
        if len(array2) <= iIndex:
            break
        if int(obj) > int(array2[iIndex]):
            return 1
        if int(obj) < int(array2[iIndex]):
            return -1
        iIndex = iIndex + 1
    return 0
