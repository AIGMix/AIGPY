#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   m3u8Helper.py
@Time    :   2019/08/23
@Author  :   Yaronzz
@Version :   2.0
@Contact :   yaronhuang@foxmail.com
@Desc    :
"""
import re

from aigpy import netHelper
from aigpy.downloadHelper import DownloadTool


def parseUrl(url: str) -> list:
    """Get ts-urls from m3u8-url"""
    content = netHelper.downloadString(url, None)
    pattern = re.compile(r"(?<=http).+?(?=\\n)")
    plist = pattern.findall(str(content))
    urlList = ["http" + item for item in plist]
    return urlList


def download(url: str, descPath: str, threadNum: int = 15) -> (bool, str):
    """Download file by m3u8-url"""
    urlList = parseUrl(url)
    if len(urlList) <= 0:
        return False, "Parse m3u8 url failed."

    tool = DownloadTool(descPath, urlList)
    check, msg = tool.start(True, threadNum)
    if not check:
        return False, msg

    return True, ""
