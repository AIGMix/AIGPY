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
import subprocess
import requests


def getOwnPath(in__file__):
    """获取进程基本目录"""
    return os.path.dirname(os.path.realpath(in__file__))

def isWindows():
    """是否为windows系统"""
    sysName = platform.system()
    return sysName == "Windows"

def isLinux():
    """是否为linux系统"""
    sysName = platform.system()
    return sysName == "Linux"

def getProcessID(name):
    """
    #Func    :   通过进程名获取进程ID，可以用`basename xxx`         
    #Param   :   name   [in]    进程名          
    #Return  :   进程ID数组(int)    
    """
    try:
        retid = []
        if isLinux():
            lines = os.popen('ps aux | grep "' + name + '" | grep -v grep').readlines()
            if len(lines) <= 0:
                return []
            for item in lines:
                array = item.split()
                retid.append(int(array[1]))
        else:
            import psutil
            pidList = list(psutil.process_iter())
            for item in pidList:
                # 样式为："psutil.Process(pid=0, name='System Idle Process', started='2019-04-01 08:38:07')"
                stri = str(item)
                stri = stri[15:-1]
                # 取名
                itname = stri[stri.find("name")+6:-1]
                indx = itname.find(",")
                if indx >= 0:
                    itname = itname[0:indx-1]
                if itname != name:
                    continue
                # 取pid
                pid = stri[stri.find("pid")+4:stri.find("name")-2]
                retid.append(int(pid))
        return retid
    except:
        return []


def killProcess(proid):
    """
    #Func    :   杀死进程       
    #Param   :   proid [in] 进程ID     
    #Return  :   True/False     
    """
    try:
        if isLinux():
            os.popen('kill -9 ' + str(proid))
            lines = os.popen('ps ' + str(proid)).readlines()
            if len(lines) <= 1:
                return True
        else:
            lines = os.popen('tasklist | findstr ' + str(proid)).readlines()
            if len(lines) <= 0:
                return True
            unread2 = os.popen('taskkill /pid %s /f' % str(proid))
        return False
    except:
        return False

def openPort(port):
    cmds = [
        "iptables -I INPUT -m state --state NEW -m tcp -p tcp --dport " + str(port) + " -j ACCEPT",
        "iptables -I INPUT -m state --state NEW -m udp -p udp --dport " + str(port) + " -j ACCEPT",
        "ip6tables -I INPUT -m state --state NEW -m tcp -p tcp --dport " + str(port) + " -j ACCEPT",
        "ip6tables -I INPUT -m state --state NEW -m udp -p udp --dport " + str(port) + " -j ACCEPT"
    ]
    for item in cmds:
        subprocess.call(item, shell=False)
