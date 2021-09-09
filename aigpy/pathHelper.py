#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   pathHelper.py
@Time    :   2018/12/17
@Author  :   Yaronzz 
@Version :   2.0
@Contact :   yaronhuang@foxmail.com
@Desc    :  
"""

import os
import shutil


def getTmpPath(basePath: str) -> str:
    """Get tmp path name like 'Tmp1'"""
    basePath = basePath.replace("\\", "/").strip().rstrip("/")
    count = 0
    path = basePath + '/Tmp' + str(count)
    while os.path.exists(path):
        count = count + 1
        path = basePath + '/Tmp' + str(count)
    return path


def mkdirs(path: str) -> bool:
    path = path.replace("\\", "/")
    path = path.strip()
    path = path.rstrip("/")
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            return True
    except:
        return False
    return True


def remove(path: str) -> bool:
    """Remove file or dir"""
    try:
        if os.path.exists(path) is False:
            return True
        if os.path.isfile(path) is True:
            os.remove(path)
        if os.path.isdir(path) is True:
            shutil.rmtree(path)
        return True
    except:
        return False


def copyFile(srcfile: str, dstfile: str) -> bool:
    if not os.path.isfile(srcfile):
        return False

    path, name = os.path.split(dstfile)
    if not os.path.exists(path):
        mkdirs(path)
    shutil.copyfile(srcfile, dstfile)
    return True


def replaceLimitChar(path: str, newChar: str) -> str:
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
    path = path.replace('\n', '')
    path = path.replace('\t', '')
    path = path.rstrip('.')
    path = path.strip(' ')
    return path


def getDirName(filepath: str) -> str:
    """e:/test/file.txt --> e:/test/"""
    filepath = filepath.replace('\\', '/')
    index = filepath.rfind('/')
    if index < 0:
        return './'
    return filepath[0:index + 1]


def getFileName(filepath: str) -> str:
    """e:/test/file.txt --> file.txt"""
    filepath = filepath.replace('\\', '/')
    index = filepath.rfind('/')
    if index < 0:
        return filepath
    return filepath[index + 1:len(filepath)]


def getFileNameWithoutExtension(filepath: str) -> str:
    """e:/test/file.txt --> file"""
    filepath = getFileName(filepath)
    index = filepath.rfind('.')
    if index < 0:
        return filepath
    return filepath[0:index]


def getFileExtension(filepath: str) -> str:
    """e:/test/file.txt --> .txt"""
    filepath = getFileName(filepath)
    index = filepath.rfind('.')
    if index < 0:
        return
    return filepath[index:len(filepath)]


def getSize(path: str) -> int:
    try:
        size = 0
        if os.path.isdir(path) is False:
            return size

        for root, dirs, files in os.walk(path):
            size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
        return size
    except:
        return 0


def getFiles(path: str) -> list:
    try:
        ret = []
        if os.path.isdir(path) is False:
            return ret

        for root, dirs, files in os.walk(path):
            root = root.replace('\\', '/')
            for item in files:
                ret.append(root + '/' + item)
        return ret
    except:
        return []
