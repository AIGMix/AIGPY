#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
@File    :   netHelper.py
@Time    :   2018/12/17
@Author  :   Yaronzz 
@Version :   2.0
@Contact :   yaronhuang@foxmail.com
@Desc    :   
'''

from urllib.request import urlopen

import re
import os
import json
import socket
import requests

from aigpy.convertHelper import convertMemoryUnitAuto, convertMemoryUnit, MemoryUnit
from aigpy.progressHelper import ProgressTool
from aigpy.pathHelper import getDirName, mkdirs

def getIpStatus(host: str, port: int, timeouts: int = 1) -> bool:
    """Check the ip status"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeouts)
        s.connect((host, port))
        s.close()
        return True
    except:
        return False


def getIP():
    """Get self-ip"""
    text = requests.get("http://txt.go.sohu.com/ip/soip").text
    ip = re.findall(r'\d+.\d+.\d+.\d+', text)[0]
    return ip


def ignoreCertificate():
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context


def getResult(code=0, msg='', data=''):
    ret = {}
    ret['code'] = code
    ret['errmsg'] = msg
    ret['data'] = data
    return json.dumps(ret)


def getSize(url: str) -> int:
    try:
        response = urlopen(url)
        info = response.info()
        dic = dict(info)
        length = dic['Content-Length']
        return int(length)
    except:
        return -1


def getUrlsSize(urls: list) -> (int, list):
    """Get urls size

    Args:
        urls (list): urls array

    Returns:
        [int]: total size
        [list]: urls size
    """
    totalSize = 0
    array = []
    for item in urls:
        size = getSize(item)
        totalSize += size
        if size < 0:
            return -1, []
        array.append(size)
    return totalSize, array


def downloadString(url: str, timeouts=(3.05, 27)):
    try:
        response = requests.get(url, timeouts)
        return response.content
    except:
        return None


def downloadJson(url: str, timeouts=(3.05, 27)):
    try:
        response = requests.get(url, timeouts)
        info = json.loads(response.content)
        return info
    except:
        return None


def downloadFileByUrls(urls: list, fileName, stimeout=3.05, showProgress=False):
    if os.access(fileName, 0):
        os.remove(fileName)

    progress = None
    if showProgress:
        progress = ProgressTool(len(urls), 10)

    for item in urls:
        ret, ex = downloadFile(item, fileName, stimeout, False, append=True)
        if ret is not True or ex is not None:
            return False
        if showProgress:
            progress.step()
    return True


def downloadFile(url: str, fileName: str, stimeout=3.05, showProgress: bool = False, append: bool = False):
    try:
        response = urlopen(url, timeout=stimeout)

        totalSize = response.length
        fileSize, unit = convertMemoryUnitAuto(totalSize, MemoryUnit.BYTE, MemoryUnit.MB)
        if showProgress:
            progress = ProgressTool(fileSize, 15, unit=unit.name)

        # mkdir
        path = getDirName(fileName)
        mkdirs(path)

        curcount = 0
        chunksize = 16 * 1024
        mode = 'wb' if not append else 'ab'
        with open(fileName, mode) as f:
            while True:
                chunk = response.read(chunksize)
                curcount += len(chunk)
                if showProgress:
                    progress.setCurCount(convertMemoryUnit(curcount, MemoryUnit.BYTE, unit))
                f.write(chunk)
                if curcount >= totalSize:
                    break
            return True, None
    except Exception as e:
        return False, e
