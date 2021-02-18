#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   m3u8Helper.py
@Time    :   2019/08/23
@Author  :   Yaronzz 
@Version :   2.0
@Contact :   yaronhuang@foxmail.com
@Desc    :   
'''
import re
from aigpy import netHelper
from aigpy.downloadHelper import DownloadTool


def parseUrl(url: str) -> list:
    '''Get ts-urls from m3u8-url'''
    content = netHelper.downloadString(url, None)
    pattern = re.compile(r"(?<=http).+?(?=\\n)")
    plist   = pattern.findall(str(content))
    urllist = ["http" + item for item in plist]
    return urllist


def download(url: str, descpath: str, threadnum: int = 15) -> (bool, str):
    '''Download file by m3u8-url'''
    urllist = parseUrl(url)
    if len(urllist) <= 0:
        return False, "Parse m3u8 url failed."
    
    tool = DownloadTool(descpath, urllist)
    check, msg = tool.start(True, threadnum)
    if not check:
        return False, msg
    
    return True, ""



