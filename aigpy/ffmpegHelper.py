#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ffmpegHelper.py
@Time    :   2018/12/17
@Author  :   Yaron Huang 
@Version :   1.0
@Contact :   yaronhuang@qq.com
@Desc    :   
'''

import os
import re
import sys
import shutil
import subprocess

import aigpy.netHelper as netHelper
import aigpy.pathHelper as pathHelper
import aigpy.threadHelper as threadHelper

from aigpy.progressHelper import ProgressTool

class FFmpegTool(object):
    def __init__(self, threadNum=50):
        self.thread        = threadHelper.ThreadTool(threadNum)
        self.waitCount     = 0
        self.completeCount = 0
        self.progress      = None
        return
    
    def __thradfunc_dl(self, url, filepath, retrycount):
        check = False
        try:
            while retrycount > 0:
                retrycount = retrycount - 1
                check = netHelper.downloadFile(url, filepath)
                if check:
                    break
        except:
            pass
        self.completeCount = self.completeCount + 1
        self.progress.step()
        return

    
    def __parseM3u8(self, url):
        content = netHelper.downloadString(url, None)
        pattern = re.compile(r"(?<=http).+?(?=\\n)")
        plist = pattern.findall(str(content))
        urllist = []
        for item in plist:
            urllist.append("http"+item)
        return urllist

    def mergerByM3u8_Multithreading(self, url, filepath, showprogress=False, showshell=False):
        try:
            # Get urllist
            urllist = self.__parseM3u8(url)
            if len(urllist) <= 0:
                return False

            # Creat tmpdir
            path = pathHelper.getDirName(filepath)
            tmpPath = pathHelper.getDiffTmpPathName(path)
            if pathHelper.mkdirs(tmpPath) == False:
                return False
            
            # Progress
            self.progress = None
            if showprogress:
                self.progress = ProgressTool(len(urllist))

            # Download files
            index              = 0
            allpath            = []
            self.waitCount     = len(urllist)
            self.completeCount = 0
            for item in urllist:
                index = index + 1
                path = tmpPath + '\\' + str(index) + ".mp4"
                allpath.append(path)
                if os.path.exists(path):
                    os.remove(path)
                self.thread.start(self.__thradfunc_dl, item, path, 3)
            self.thread.waitAll()
            self.mergerByFiles(allpath, filepath, showshell)
            shutil.rmtree(tmpPath)
            return True
        except:
            return False

    def mergerByM3u8(self, url, filepath, showshell=False):
        try:
            cmd = "ffmpeg -safe 0 -i " + url + " -c copy -bsf:a aac_adtstoasc \"" + filepath + "\""
            if showshell:
                res = subprocess.call(cmd, shell=True)
            else:
                res = subprocess.call(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if res != 0:
                return False
            return True
        except:
            return False

    def mergerByFiles(self, srcfilepaths, filepath, showshell=False):
        result = True
        tmpfile = filepath + "TMP.txt"
        try:
            with open(tmpfile, 'w') as fd:
                for item in srcfilepaths:
                    fd.write('file \'' + item + '\'\n')

            cmd = "ffmpeg -f concat -safe 0 -i \"" + tmpfile + "\" -c copy \"" + filepath + "\""
            if showshell:
                res = subprocess.call(cmd, shell=True)
            else:
                res = subprocess.call(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if res != 0:
                result = False
        except:
            result = False

        if os.access(tmpfile,0):
            os.remove(tmpfile)
        return result




