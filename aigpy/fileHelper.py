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
import json
import hashlib
from aigpy.pathHelper import getDirName, mkdirs


def getSize(path: str) -> int:
    if not os.path.isfile(path):
        return 0
    return os.path.getsize(path)


def getHash(path: str, blockSize=2 * 1024 * 1024) -> str:
    with open(path, 'rb') as f:
        sha1 = hashlib.sha1()
        while True:
            data = f.read(blockSize)
            if not data:
                break
            sha1.update(data)
        return sha1.hexdigest()
    return ''


def getContent(path: str, isBin=False):
    size = getSize(path)
    if size <= 0:
        return ""

    mode = 'r' if not isBin else "rb"
    with open(path, mode) as fd:
        content = fd.read(size)
    return content


def getJson(path):
    try:
        with open(path, 'rb') as f:
            text = f.read().decode('utf-8')
            return json.loads(text)
    except:
        return {}


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


def writeJson(path: str, data: dict):
    try:
        with open(path, 'w') as f:
            f.write(json.dumps(data))
            f.flush()
        return True
    except:
        return False


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
