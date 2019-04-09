#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   logHelper.py
@Time    :   2019/02/28
@Author  :   Yaron Huang 
@Version :   1.0
@Contact :   yaronhuang@qq.com
@Desc    :   LOG FILE TOOL
'''
import os
import time

def write(path, string):
    """
    #Func    :   写日志              
    #Param   :   path       [in] 日志文件路径           
    #Param   :   string     [in] 日志字符窗         
    #Return  :   True/False     
    """
    try:
        fd = open(path, 'a+')
        fd.write(string + '\n')
        fd.close()
        return True
    except:
        return False  

def writeByTime(path, string):
    """
    #Func    :   写日志(带日期时间)         
    #Param   :   path       [in] 日志文件路径               
    #Param   :   string     [in] 日志字符窗         
    #Return  :   True/False     
    """
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return write(path, '[' + date + ']  ' + string)
 
def clear(path):
    """
    #Func    :   清除日志文件       
    #Param   :   path       [in] 日志文件路径       
    """
    try:
        os.remove(path)
    except:
        pass
