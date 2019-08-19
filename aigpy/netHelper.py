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
from aigpy.progressHelper import ProgressTool
from socket import *
from aigpy.convertHelper import convertStorageUnit
from aigpy.pathHelper import getFileName

def downloadString(url, timeouts=(3.05, 27)):
    """
    #Func    :   下载字符串        
    #Param   :   url        [in] 链接       
    #Param   :   timeouts   [in] 超时             
    #Return  :   Err:None              
    """
    try:
        re = requests.get(url, timeouts)
        return re.content
    except:
        return None 
    

def downloadJson(url, timeouts=(3.05, 27)):
    """
    #Func    :   下载json   
    #Param   :   url        [in] 链接       
    #Param   :   timeouts   [in] 超时       
    #Return  :   Err:None       
    """
    try:
        re = requests.get(url, timeouts)
        info = json.loads(re.content)
        return info
    except:
        return None

def getFileSize(url):
    """
    #Func    :   获取文件大小       
    #Param   :   url    [in] 链接           
    #Return  :   Err:-1     
    """
    if sys.version_info > (3, 0):
        from urllib.request import urlopen
    else:
        from urllib2 import urlopen

    try:
        response = urlopen(url)
        info     = response.info()
        dic      = dict(info)
        length   = dic['Content-Length']
        return int(length)
    except:
        return -1

def downloadFile(url, fileName, stimeout=None, showprogress=False):
    """
    #Func    :   下载文件              
    #Param   :   url        [in] 链接       
    #Param   :   fileName   [in] 文件路径              
    #Return  :   True/False            
    """
    if sys.version_info > (3,0):
        from urllib.request import urlopen
    else:
        from urllib2 import urlopen
    
    try:
        if timeout is None:
            response = urlopen(url)
        else:
            response = urlopen(url, timeout=stimeout)
        
        unit = 'mb'
        if convertStorageUnit(response.length, 'byte', unit) < 1:
            unit = 'kb'
        progress = None
        if showprogress:
            desc = getFileName(fileName)
            progress = ProgressTool(convertStorageUnit(response.length, 'byte', unit), 10, unit=unit, desc=desc)

        curcount  = 0
        chunksize = 16 * 1024
        with open(fileName, 'wb') as f:
            while True:
                chunk = response.read(chunksize)
                curcount += len(chunk)
                if progress:
                    progress.setCurCount(convertStorageUnit(curcount, 'byte', unit))
                if not chunk:
                    break
                f.write(chunk)
            return True
    except:
        return False

def getIpStatus(host, port, timeouts=1):
    """
    #Func    :   测试连接              
    #Param   :   host        [in] IP地址       
    #Param   :   port        [in] 端口       
    #Param   :   timeouts    [in] 超时       
    #Return  :   True/False       
    """
    setdefaulttimeout(timeouts)
    flag = True
    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((host, port))
        s.close()
    except:
        flag = False
    return flag



