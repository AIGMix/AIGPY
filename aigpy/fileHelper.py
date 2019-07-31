#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   fileHelper.py
@Time    :   2019/03/11
@Author  :   Yaron Huang 
@Version :   1.0
@Contact :   yaronhuang@qq.com
@Desc    :   
'''

import os

def getFileSize(path):
    """
    #Func    :   获取文件大小       
    #Param   :   path   [in] 文件路径
    #Return  :   整数       
    """
    try:
        if os.path.isfile(path) is False:
            return 0
        return os.path.getsize(path)
    except:
        return 0

def getFileContent(path, isBin = False):
    """
    #Func    :   获取文件全部内容   
    #Param   :   path    [in] 文件路径
    #Param   :   isBin   [in] 是否用二进制读取
    #Return  :   整数
    """
    mode = 'r'
    if isBin:
        mode = 'rb'
    try:
        size = getFileSize(path)
        if size <= 0:
            return ""
        with open(path, mode) as fd:
            content = fd.read(size) 
        return content
    except:
        return ""