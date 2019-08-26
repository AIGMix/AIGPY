#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   m3u8Helper.py
@Time    :   2019/08/23
@Author  :   Yaron Huang 
@Version :   1.0
@Contact :   yaronhuang@qq.com
@Desc    :   
'''
import re
from aigpy import netHelper

def getM3u8TsUrls(url):
    content = netHelper.downloadString(url, None)
    pattern = re.compile(r"(?<=http).+?(?=\\n)")
    plist   = pattern.findall(str(content))
    urllist = []
    for item in plist:
        urllist.append("http"+item)
    return urllist




# url = 'http://api.tidal.com/v1/videos/92418079/hls/CAEQARgDIP___________wEouA8yQzgyNjFkMWZmLTYwNmEtNDNkNy04YzFjLTA0YzVhNzI3YzllZV8xMjgvbWVkaWFfcGxheWxpc3RfMjUwNTIxLm0zdTg=.m3u8?authtoken=exp~1566527826000.hmac~U5uKekcIxE_cqhGcp9HJ70kYV3d7qWQUv8FTQiSezz0='
# getM3u8TsUrls(url)