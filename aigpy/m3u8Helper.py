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
import shutil
from aigpy import netHelper
from aigpy.progressHelper import ProgressTool
from aigpy.pathHelper import getDirName, getDiffTmpPathName, mkdirs
from aigpy.threadHelper import ThreadTool
from aigpy.fileHelper import getFileContent

def paresUrl(url):
    content = netHelper.downloadString(url, None)
    pattern = re.compile(r"(?<=http).+?(?=\\n)")
    plist   = pattern.findall(str(content))
    urllist = []
    for item in plist:
        urllist.append("http"+item)
    return urllist

def __threadfunc__(url, filepath, progress):
    retrycount = 3
    try:
        while retrycount > 0:
            retrycount = retrycount - 1
            check = netHelper.downloadFile(url, filepath, 30)
            if check:
                break
    except:
        pass
    progress.step()


def __merger__(files, filepath):
    try:
        with open(filepath, "wb") as fd:
            for item in files:
                data = getFileContent(item, True)
                fd.write(data)
        return True
    except:
        return False
    

def download(url, descpath, threadnum = 15):
    try:
        urllist = paresUrl(url)
        if len(urllist) <= 0:
            return False
        
        threads = ThreadTool(threadnum)

        # Creat tmpdir
        path = getDirName(descpath)
        tmpPath = getDiffTmpPathName(path)
        if mkdirs(tmpPath) is False:
            return False

        # Progress
        progress = ProgressTool(len(urllist), 20)

        # Download files
        files = []
        for i, item in enumerate(urllist):
            filepath = tmpPath + '/' + str(i) + '.ts'
            files.append(filepath)
            threads.start(__threadfunc__, item, filepath, progress)
        threads.waitAll()

        # merger
        __merger__(files, descpath)
        shutil.rmtree(tmpPath)
        threads.close()
        return True
    except:
        shutil.rmtree(tmpPath)
        return False


