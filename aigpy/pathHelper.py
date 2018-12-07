#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   pathHelper.py
@Time    :   2018/12/17
@Author  :   Yaron Huang 
@Version :   1.0
@Contact :   yaronhuang@qq.com
@Desc    :   
'''

import os

def getDiffTmpPathName(basePath):
    count = 0
    basePath = basePath.strip()
    basePath = basePath.rstrip("\\")
    path = basePath + '\\Tmp' + str(count)
    while os.path.exists(path):
        count = count + 1
        path = basePath + '\\Tmp' + str(count)
    return path

def mkdirs(path):
    path = path.strip()
    path = path.rstrip("\\")
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    return False

def replaceLimitChar(path, newChar):
    if path is None:
        return ""
    if newChar is None:
        newChar = ''
    path = path.replace(':', newChar)
    path = path.replace('/', newChar)
    path = path.replace('?', newChar)
    path = path.replace('<', newChar)
    path = path.replace('>', newChar)
    path = path.replace('|', newChar)
    path = path.replace('\\', newChar)
    path = path.replace('*', newChar)
    path = path.replace('\"', newChar)
    return path

def getDirName(filepath):
    filepath = filepath.replace('\\', '/')
    index    = filepath.rfind('/')
    if index == -1:
        return './'
    return filepath[0:index+1]

def getFileName(filepath):
    filepath = filepath.replace('\\', '/')
    index = filepath.rfind('/')
    if index == -1:
        return filepath
    return filepath[index+1:len(filepath)]

def getFileNameWithoutExtension(filepath):
    filepath = getFileName(filepath)
    index = filepath.rfind('.')
    if index == -1:
        return filepath
    return filepath[0:index]

def getFileExtension(filepath):
    filepath = getFileName(filepath)
    index = filepath.rfind('.')
    if index == -1:
        return
    return filepath[index:len(filepath)]


