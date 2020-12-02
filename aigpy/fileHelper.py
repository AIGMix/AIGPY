#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   fileHelper.py
@Time    :   2019/03/11
@Author  :   Yaronzz 
@Version :   2.0
@Contact :   yaronhuang@foxmail.com
@Desc    :   
'''

import os


def getFileSize(path):
    try:
        if not os.path.isfile(path):
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


def getFileLines(path):
    content = getFileContent(path)
    if content == "":
        return []
    lines = content.split('\n')
    return lines


def write(path, content, mode):
    try:
        with open(path, mode) as fd:
            fd.write(content)
        return True
    except:
        return False


def writeLines(path, lines:list, mode):
    content = ""
    for item in lines:
        content += item + '\n'
    return write(path, content, mode)

