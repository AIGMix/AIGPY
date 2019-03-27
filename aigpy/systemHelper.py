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

def getProcessID(name):
    """
    #Func    :   通过进程名获取进程ID，可以用`basename xxx`         
    #Param   :   name   [in]    进程名          
    #Return  :   进程ID数组(int)
    """
    try:
        lines = os.popen('ps aux | grep "' + name + '" | grep -v grep').readlines()
        if len(lines) <= 0:
            return []
        id = []
        for item in lines:
            array = item.split()
            id.append(int(array[1]))
        return id
    except:
        return []

def killProcess(id):
    """
    #Func    :   杀死进程       
    #Param   :   id [in] 进程ID     
    #Return  :   True/False     
    """
    try:
        os.popen('kill -9 ' + str(id))
        lines = os.popen('ps ' + str(id)).readlines()
        if len(lines) <= 1:
            return True
        return False
    except:
        return False


