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
    try:
        if os.path.isfile(path) is False:
            return 0
        return os.path.getsize(path)
    except:
        return 0


def getFileContent(path, isBin=False):
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


def write(path, content, mode):
    try:
        with open(path, mode) as fd:
            fd.write(content)
        return True
    except Exception as e:
        return False
