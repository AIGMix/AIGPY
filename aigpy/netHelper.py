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
from aigpy.fileHelper import getFileContent, writeLines, getFileLines
from aigpy.LockHelper import LockHelper
import aigpy.stringHelper as AIGString
import aigpy.fileHelper as AIGFile
import aigpy.netHelper as AIGNet
import aigpy.convertHelper as AIGConvert


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
            curcount += 1
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
            desc = ""  # getFileName(fileName)
            progress = ProgressTool(convertStorageUnit(response.length, 'byte', unit), 15, unit=unit, desc=desc)

        mode = 'wb'
        if append:
            mode = 'ab'

        # mkdir
        path = getDirName(fileName)
        mkdirs(path)

        curcount = 0
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


def __downloadPartFile__(url, fileName, stimeout=None, start=None, length=None, progress=None, unit='mb', retry=3):
    while retry > 0:
        try:
            headers = None
            if start is not None and length is not None:
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
            if retry <= 0:
                return False, e
            retry -= 1
    return False, "retry num must > 0."


def __mergerPartFiles__(files, filepath):
    try:
        with open(filepath, "wb") as fd:
            for item in files:
                data = getFileContent(item, True)
                fd.write(data)
        return True
    except:
        return False


def __checkFiles__(files):
    for item in files:
        if os.path.isfile(files):
            continue
        else:
            return False
    return True


def downloadFileMultiThread(url, fileName, stimeout=None, showprogress=False, threadnum=30, partsize=1048576):
    try:
        filelength = getFileSize(url)
        if filelength <= 0:
            return False, "File size = " + str(filelength)

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
            return False, "Creat tmpdir failed:" + tmpPath

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

        #check and merger
        errmsg = ""
        flag = __checkFiles__(files)
        if flag is False:
            errmsg = "Merger files failed, some files download failed."
        else:
            flag = __mergerPartFiles__(files, fileName)
            if flag is False:
                errmsg = "Merger files failed."

        shutil.rmtree(tmpPath)
        threads.close()
        return flag, errmsg

    except Exception as e:
        shutil.rmtree(tmpPath)
        threads.close()
        return False, e


def __downloadPartFile2__(lock: LockHelper, url, fileName, stimeout=None, start=None, length=None, progress=None, unit='mb', retry=3):
    isLock = False
    while retry > 0:
        try:
            headers = None
            if start is not None and length is not None:
                rang = 'bytes=%s-%s' % (start, start + length - 1)
                headers = {'Range': rang}

            res = requests.get(url, headers=headers, timeout=stimeout)
            res.raise_for_status()

            # mkdir
            path = getDirName(fileName)
            mkdirs(path)

            lock.write_acquire()
            isLock = True
            with open(fileName, 'rb+') as f:
                f.seek(start)
                f.write(res.content)
                writeLines(fileName + ".result", ["index=" + str(start) + ",length=" + str(length)], "a")
            lock.write_release()
            isLock = False


            if progress is not None:
                progress.addCurCount(convertStorageUnit(length, 'byte', unit))
            return True, None
        except Exception as e:
            if isLock:
                lock.write_release()
                isLock = False
            if retry <= 0:
                return False, e
            retry -= 1
    return False, "retry num must > 0."


def downloadFileMultiThread2(url, fileName, stimeout=None, showprogress=False, threadnum=30, partsize=1048576):
    try:
        fileResult = fileName + '.result'
        filelength = getFileSize(url)
        if filelength <= 0:
            return False, "File size = " + str(filelength)

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

        # Creat dir
        path = getDirName(fileName)
        if mkdirs(path) is False:
            return False, "Creat path failed:" + path

        # Creat empty file
        with open(fileName, 'wb') as fd:
            fd.seek(filelength - 1)
            fd.write(b'\x00')

        if os.path.isfile(fileResult):
            os.unlink(fileResult)

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

        lock = LockHelper()
        for i, item in enumerate(rangs):
            threads.start(__downloadPartFile2__, lock, url, fileName, stimeout, item[0], item[1], progress, unit)
        threads.waitAll()
        threads.close()

        lines = getFileLines(fileResult)
        if os.path.isfile(fileResult):
            os.unlink(fileResult)
        if len(lines) != len(rangs) + 1:
            return False, "Some parts download failed."
        return True, ""

    except Exception as e:
        if os.path.isfile(fileResult):
            os.unlink(fileResult)
        if os.path.isfile(fileName):
            os.unlink(fileName)
        return False, e



# downloadFileMultiThread2("https://down5.huorong.cn/sysdiag-full-5.0.54.7-20201115.exe", "./test/tt.exe", showprogress=True)
