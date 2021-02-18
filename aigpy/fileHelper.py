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
from aigpy.pathHelper import getDirName, mkdirs


def getSize(path: str) -> int:
    if not os.path.isfile(path):
        return 0
    return os.path.getsize(path)


def getContent(path: str, isBin=False):
    size = getSize(path)
    if size <= 0:
        return ""

    mode = 'r' if not isBin else "rb"
    with open(path, mode) as fd:
        content = fd.read(size)
    return content


def getLines(path: str) -> list:
    content = getContent(path)
    if content == "":
        return []
    return content.split('\n')


def write(path: str, content, mode: str):
    try:
        with open(path, mode) as fd:
            fd.write(content)
        return True
    except:
        return False


def writeLines(path: str, lines: list, mode):
    content = "\n".join(lines)
    return write(path, content, mode)


def CreateEmptyFile(filePath: str, size: int):
    try:
        # Create dir
        path = getDirName(filePath)
        if mkdirs(path) is False:
            return False

        # Create empty file
        with open(filePath, 'wb') as fd:
            fd.seek(size - 1)
            fd.write(b'\x00')
        return True
    except:
        return False

