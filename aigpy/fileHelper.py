#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   fileHelper.py
@Time    :   2019/03/11
@Author  :   Yaronzz 
@Version :   2.0
@Contact :   yaronhuang@foxmail.com
@Desc    :  
"""

import hashlib
import json
import os

from aigpy.pathHelper import getDirName, mkdirs


def getSize(path: str) -> int:
    if not os.path.isfile(path):
        return 0
    return os.path.getsize(path)


def getHash(path: str, blockSize: int = 2 * 1024 * 1024) -> str:
    with open(path, 'rb') as f:
        sha1 = hashlib.sha1()
        while True:
            data = f.read(blockSize)
            if not data:
                break
            sha1.update(data)
        return sha1.hexdigest()


def getMD5(path: str):
    m = hashlib.md5()
    with open(path, 'rb') as fp:
        while True:
            data = fp.read(4096)
            if not data:
                break
            m.update(data)

    return m.hexdigest()


def getContent(path: str, isBin: bool = False, encoding: str = None):
    size = getSize(path)
    if size <= 0:
        return ""

    mode = 'r' if not isBin else "rb"
    with open(path, mode, encoding=encoding) as fd:
        content = fd.read(size)
    return content


def getJson(path, encoding: str = None):
    try:
        with open(path, 'r', encoding=encoding) as f:
            text = f.read()
            return json.loads(text)
    except:
        return {}


def getLines(path: str, encoding: str = None) -> list:
    content = getContent(path, False, encoding)
    if content == "":
        return []
    return content.split('\n')


def write(path: str, content, mode: str, encoding: str = None):
    try:
        with open(path, mode, encoding=encoding) as fd:
            fd.write(content)
        return True
    except:
        return False


def writeLines(path: str, lines: list, mode: str, encoding: str = None):
    content = "\n".join(lines)
    return write(path, content, mode, encoding)


def writeJson(path: str, data: dict, encoding: str = None):
    try:
        with open(path, 'w', encoding=encoding) as f:
            f.write(json.dumps(data))
            f.flush()
        return True
    except:
        return False


def createEmptyFile(filePath: str, size: int):
    try:
        # Create dir
        path = getDirName(filePath)
        if mkdirs(path) is False:
            return False

        # Create empty file
        fp = open(filePath, "wb")
        fp.truncate(size)
        fp.close()
        return True
    except:
        return False
