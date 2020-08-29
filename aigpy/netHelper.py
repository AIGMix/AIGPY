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

import re
import os
import sys
import json
import socket
import requests
import shutil
from urllib.request import urlopen
from aigpy.progressHelper import ProgressTool
from aigpy.convertHelper import convertStorageUnit
from aigpy.pathHelper import getFileName, getDirName, mkdirs, getDiffTmpPathName
from aigpy.threadHelper import ThreadTool
from aigpy.fileHelper import getFileContent


def getIpStatus(host, port, timeouts=1):
    socket.setdefaulttimeout(timeouts)
    flag = True
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.close()
    except:
        flag = False
    return flag


def getIP():
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


def getFileSize(url):
    try:
        response = urlopen(url)
        info = response.info()
        dic = dict(info)
        length = dic['Content-Length']
        return int(length)
    except:
        return -1


def downloadString(url, timeouts=(3.05, 27)):
    try:
        re = requests.get(url, timeouts)
        return re.content
    except:
        return None 
    

def downloadJson(url, timeouts=(3.05, 27)):
    try:
        re = requests.get(url, timeouts)
        info = json.loads(re.content)
        return info
    except:
        return None


def downloadFileByUrls(urlArray, fileName, stimeout=None, showprogress=False):
    if os.access(fileName, 0):
        os.remove(fileName)

    progress = None
    if showprogress:
        desc = getFileName(fileName)
        progress = ProgressTool(len(urlArray), 10, unit='', desc=desc)

    curcount = 1    
    for item in urlArray:
        ret, ex = downloadFile(item, fileName, stimeout, False, append=True)
        if ret != True or ex != None:
            return False
        if progress:
            progress.setCurCount(curcount)
            curcount+=1
    return True


def downloadFile(url, fileName, stimeout=None, showprogress=False, append=False):
    try:
        if stimeout is None:
            response = urlopen(url)
        else:
            response = urlopen(url, timeout=stimeout)
        
        unit = 'mb'
        if convertStorageUnit(response.length, 'byte', unit) < 1:
            unit = 'kb'
        progress = None
        if showprogress:
            desc = ""#getFileName(fileName)
            progress = ProgressTool(convertStorageUnit(response.length, 'byte', unit), 15, unit=unit, desc=desc)

        mode ='wb'
        if append:
            mode = 'ab'

        # mkdir
        path = getDirName(fileName)
        mkdirs(path)

        curcount  = 0
        chunksize = 16 * 1024
        with open(fileName, mode) as f:
            while True:
                chunk = response.read(chunksize)
                curcount += len(chunk)
                if progress:
                    progress.setCurCount(convertStorageUnit(curcount, 'byte', unit))
                if not chunk:
                    break
                f.write(chunk)
            return True, None
    except Exception as e:
        return False, e


def __downloadPartFile__(url, fileName, stimeout=None, start=None, length=None, progress = None, unit = 'mb'):
    try:
        headers = None
        if start != None and length != None:
            rang = 'bytes=%s-%s' % (start, start + length - 1)
            headers = {'Range': rang}
        
        res = requests.get(url, headers=headers, timeout=stimeout)
        res.raise_for_status()

        # mkdir
        path = getDirName(fileName)
        mkdirs(path)

        with open(fileName, 'wb') as f:
            f.write(res.content)

        if progress is not None:
            progress.addCurCount(convertStorageUnit(length, 'byte', unit))
        return True, None
    except Exception as e:
        if os.path.isfile(fileName):
            os.unlink(fileName)
        return False, e


def __mergerPartFiles__(files, filepath):
    try:
        with open(filepath, "wb") as fd:
            for item in files:
                data = getFileContent(item, True)
                fd.write(data)
        return True
    except:
        return False


def downloadFileMultiThread(url, fileName, stimeout=None, showprogress=False, threadnum=30, partsize=1048576):
    try:
        filelength = getFileSize(url)
        if filelength <= 0:
            return False, None

        at = 0
       	rangs = []
        length = filelength
        while length > 0:
            if length > partsize:
                bf = [at, partsize]
            else:
                bf = [at, length]
            rangs.append(bf)
            at += partsize
            length -= partsize

        # Creat tmpdir
        path = getDirName(fileName)
        tmpPath = getDiffTmpPathName(path)
        if mkdirs(tmpPath) is False:
            return False, None

        # thread
        threads = ThreadTool(threadnum)
        # Progress
        unit = 'mb'
        if convertStorageUnit(filelength, 'byte', unit) < 1:
            unit = 'kb'
        progress = None
        if showprogress:
            desc = ""  # getFileName(fileName)
            progress = ProgressTool(convertStorageUnit(filelength, 'byte', unit), 15, unit=unit, desc=desc)

        files = []
        for i, item in enumerate(rangs):
            filepath = tmpPath + '/' + str(i) + '.part'
            files.append(filepath)
            threads.start(__downloadPartFile__, url, filepath, stimeout, item[0], item[1], progress, unit)
        threads.waitAll()

        # merger
        flag = __mergerPartFiles__(files, fileName)
        shutil.rmtree(tmpPath)
        threads.close()
        return flag, None

    except Exception as e:
        shutil.rmtree(tmpPath)
        threads.close()
        return False, e
