#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   netHelper.py
@Time    :   2018/12/17
@Author  :   Yaron Huang 
@Version :   1.0
@Contact :   yaronhuang@qq.com
@Desc    :   
'''

import sys
import requests
import json
from socket import *

def downloadString(url, timeout=(3.05, 27)):
    try:
        re = requests.get(url, timeout)
        return re.content
    except:
        return
    
def downloadJson(url, timeout=(3.05, 27)):
    try:
        re = requests.get(url, timeout)
        info = json.loads(re.content)
        return info
    except:
        return

def getFileSize(url):
    """
    #Func    :   获取文件大小       
    #Param   :   url    [in] 链接       
    #Return  :   Err:-1     
    """
    if sys.version_info > (2, 7):
        from urllib.request import urlopen
    else:
        from urllib2 import urlopen

    try:
        response = urlopen(url)
        dic    = dict(response.header)
        length = dic['Content-Length']
        return length
    except:
        return -1

def downloadFile(url, fileName):
    if sys.version_info > (2, 7):
        from urllib.request import urlopen
    else:
        from urllib2 import urlopen

    try:
        response = urlopen(url)
        chunk = 16 * 1024
        with open(fileName, 'wb') as f:
            while True:
                chunk = response.read(chunk)
                if not chunk:
                    break
                f.write(chunk)
            return True
    except:
        return False

def getIpStatus(host, port, timeout=1):
    setdefaulttimeout(timeout)
    flag = True
    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((host, port))
        s.close()
    except:
        flag = False
    return flag
