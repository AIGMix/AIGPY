#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#coding:utf-8
'''
@File    :   ffmpegHelper.py
@Time    :   2018/12/17
@Author  :   Yaronzz 
@Version :   2.0
@Contact :   yaronhuang@foxmail.com
@Desc    :   
'''

import os
import re
import sys
import shutil
import subprocess
import aigpy.fileHelper as fileHelper
import aigpy.systemHelper as systemHelper
import aigpy.netHelper as netHelper
import aigpy.pathHelper as pathHelper
import aigpy.threadHelper as threadHelper
from   aigpy.progressHelper import ProgressTool

class FFmpegTool(object):
    def __init__(self, threadNum=50, mergerTimeout=None):
        """
        #Func    :   初始化             
        #Param   :   threadNum     [in] 线程数          
        #Param   :   mergerTimeout [in] 超时 秒     
        #Return  :   True/False             
        """
        self.thread        = threadHelper.ThreadTool(threadNum)
        self.waitCount     = 0
        self.completeCount = 0
        self.progress      = None
        self.mergerTimeout = mergerTimeout
        self.enable        = self._checkTool()
        return
    
    def __thradfunc_dl(self, url, filepath, retrycount):
        check = False
        try:
            while retrycount > 0:
                retrycount = retrycount - 1
                check = netHelper.downloadFile(url, filepath, 30)
                if check:
                    break
        except:
            pass
        self.completeCount = self.completeCount + 1
        if self.progress is not None:
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

    def __process(self, cmd, retrycount, showshell, filename, removeFile=True):
        stdoutFile = None
        fp = None
        while retrycount >= 0:
            retrycount -= 1
            try:
                if showshell:
                    if sys.version_info[0] > 2:
                        res = subprocess.call(cmd, timeout=self.mergerTimeout, shell=True)
                    else:
                        cmd = cmd.encode(sys.getfilesystemencoding())
                        res = subprocess.call(cmd, shell=True)
                else:
                    exten = pathHelper.getFileExtension(filename)
                    stdoutFile = filename.replace(exten, '-stdout.txt')
                    fp  = open(stdoutFile, 'w')
                    if sys.version_info[0] > 2:
                        res = subprocess.call(cmd, timeout=self.mergerTimeout, shell=True, stdout=fp, stderr=fp)
                    else:
                        res = subprocess.call(cmd, shell=True, stdout=fp, stderr=fp)
                    fp.close()
                    fp = None
                    pathHelper.remove(stdoutFile)
                if res == 0:
                    return True
            except:
                pass
            if fp:
                fp.close()
            pathHelper.remove(stdoutFile)
            if removeFile: 
                pathHelper.remove(filename)
        return False

    def mergerByM3u8_Multithreading2(self, url, filepath, showprogress=False, showshell=False):
        try:
            # Get urllist
            urllist = self.__parseM3u8(url)
            if len(urllist) <= 0:
                return False

            sdir = pathHelper.getDirName(filepath)
            pathHelper.mkdirs(sdir)

            ext    = pathHelper.getFileExtension(filepath)
            tspath = filepath.replace(ext, '.ts')
            pathHelper.remove(tspath)
            if not netHelper.downloadFileByUrls(urllist, tspath, 30, True):
                return False
            if self.covertFile(tspath, filepath):
                pathHelper.remove(tspath)
                return True
            return False
        except:
            return False

    def mergerByM3u8_Multithreading(self, url, filepath, showprogress=False, showshell=False):
        """
        #Func    :   多线程下载并合并文件(使用M3u8的url)        
        #Param   :   url             [in] 链接
        #Param   :   filepath        [in] 目标文件名
        #Param   :   showprogress    [in] 是否显示进度条
        #Param   :   showshell       [in] 是否显示cmd信息
        #Return  :   True/False
        """
        try:
            # Get urllist
            urllist = self.__parseM3u8(url)
            if len(urllist) <= 0:
                return False

            # Creat tmpdir
            path    = pathHelper.getDirName(filepath)
            tmpPath = pathHelper.getDiffTmpPathName(path)
            if pathHelper.mkdirs(tmpPath) is False:
                return False
            
            # Progress
            self.progress = None
            if showprogress:
                self.progress = ProgressTool(len(urllist))

            # Download files
            allpath            = []
            self.waitCount     = len(urllist)
            self.completeCount = 0
            for i, item in enumerate(urllist):
                index = i + 100001
                path  = tmpPath + '/' + str(index) + ".ts"
                path  = os.path.abspath(path)
                allpath.append(path)
                if os.path.exists(path):
                    os.remove(path)
                self.thread.start(self.__thradfunc_dl, item, path, 3)
            self.thread.waitAll()
            ret = self.mergerByTs(tmpPath, filepath, showshell)
            # ret = self.mergerByFiles(allpath, filepath, showshell)
            shutil.rmtree(tmpPath)
            return ret
        except:
            return False

    def mergerByM3u8(self, url, filepath, showshell=False):
        """
        #Func    :   合并文件(使用M3u8的url)        
        #Param   :   url         [in] 链接       
        #Param   :   filepath    [in] 目标文件名            
        #Param   :   showshell   [in] 是否显示cmd信息              
        #Return  :   True/False 
        """
        res = -1
        try:
            filepath = os.path.abspath(filepath)
            cmd = "ffmpeg -safe 0 -i " + url + " -c copy -bsf:a aac_adtstoasc \"" + filepath + "\""
            res = self.__process(cmd, 3, showshell, filepath)
        except:
            pass
        return res

    def mergerByTs(self, srcDir, filepath, showshell=False):
        srcDir   = os.path.abspath(srcDir)
        filepath = os.path.abspath(filepath)
        if os.path.exists(srcDir) is False:
            return False
        
        exten   = pathHelper.getFileExtension(filepath)
        tmppath = filepath.replace(exten, '.ts')
        if systemHelper.isWindows():
            srcDir += '\\*.ts'
            cmd = 'copy /b "' + srcDir + '" "' + tmppath + '"'
        else:
            srcDir += '/*.ts'
            cmd = 'cat ' + srcDir + ' > "' + tmppath + '"'
        
        ret = self.__process(cmd, 3, showshell, tmppath)
        if ret is True:
            cmd = "ffmpeg -i \"" + tmppath + "\" -c copy \"" + filepath + "\""
            ret = self.__process(cmd, 3, showshell, filepath)
        pathHelper.remove(tmppath)
        return ret


    def mergerByTsfiles(self, srcfilepaths, filepath, showshell=False):
        """
        #Func    :   合并ts文件             
        #Return  :   True/False         
        """
        filepath = os.path.abspath(filepath)
        exten    = pathHelper.getFileExtension(filepath)
        tmppath  = filepath.replace(exten, '.ts')
        tmppath2 = filepath.replace(exten, '2.ts')
        array    = [srcfilepaths[i:i+25] for i in range(0, len(srcfilepaths), 25)]
        pathHelper.remove(tmppath)
        pathHelper.remove(tmppath2)

        for item in array:
            for index, file in enumerate(item):
                item[index] = '"'+ file + '"'
            form = ' + '.join(item)
            if os.access(tmppath, 0):
                form = '"' + tmppath + '" + ' + form
            
            cmd = 'copy /b ' + form + ' "' + tmppath2 + '"'
            ret = self.__process(cmd, 3, showshell, tmppath2)
            if ret is False:
                break
            pathHelper.remove(tmppath)
            os.rename(tmppath2, tmppath)

        if ret is True:
            cmd = "ffmpeg -i \"" + tmppath + "\" -c copy \"" + filepath + "\""
            ret = self.__process(cmd, 3, showshell, filepath)
        pathHelper.remove(tmppath)
        pathHelper.remove(tmppath2)
        return ret

    def _checkTool(self):
        check = False
        try:
            cmd = "ffmpeg -V"
            stdoutFile = 'ffmpegcheck-stdout.txt'
            fp = open(stdoutFile, 'w')
            if sys.version_info[0] > 2:
                res = subprocess.call(cmd, timeout=self.mergerTimeout, shell=True, stdout=fp, stderr=fp)
            else:
                res = subprocess.call(cmd, shell=True, stdout=fp, stderr=fp)
            fp.close()
            txt = fileHelper.getFileContent(stdoutFile)
            if 'version' in txt and 'Copyright' in txt:
                check = True
        except:
            pass
        pathHelper.remove(stdoutFile)
        return check
    def covertFile(self, srcfile, descfile, showshell=False):
        try:
            filepath = os.path.abspath(srcfile)
            filepath2 = os.path.abspath(descfile)
            cmd = "ffmpeg -i \"" + filepath + "\" -c copy \"" + filepath2 + "\""
            ret = self.__process(cmd, 3, showshell, filepath, False)
            return ret
        except:
            return False

    def mergerByFiles(self, srcfilepaths, filepath, showshell=False):
        """
        #Func    :   合并文件       
        #Param   :   srcfilepaths   [in] 文件名数组     
        #Param   :   filepath       [in] 目标文件名     
        #Param   :   showshell      [in] 是否显示cmd信息        
        #Return  :   True/False 
        """
        filepath = os.path.abspath(filepath)
        res     = -1
        tmpfile = filepath + "TMP.txt"
        paths   = srcfilepaths
        group   = None
        groupnum= 50
        try:
            # 先分组合并，再一起合并
            if len(srcfilepaths) > groupnum:
                dirName = pathHelper.getDirName(filepath)
                group   = pathHelper.getDiffTmpPathName(dirName)
                if pathHelper.mkdirs(group) is False:
                    return False
                
                newPaths = []
                array    = [srcfilepaths[i:i+groupnum] for i in range(0, len(srcfilepaths), groupnum)]
                for index, item in enumerate(array):
                    file = group + '/' + str(index) + ".mp4"
                    newPaths.append(file)
                    if self.mergerByFiles(item, file, showshell) is False:
                        return False
                paths = newPaths

            # 创建临时文件,将要合并的文件名列表写入
            with open(tmpfile, 'w') as fd:
                for item in paths:
                    item = os.path.abspath(item)
                    fd.write('file \'' + item + '\'\n')


            # 调用ffmpeg进行合并
            cmd = "ffmpeg -f concat -safe 0 -i \"" + tmpfile + "\" -c copy \"" + filepath + "\""
            res = self.__process(cmd, 3, showshell, filepath)
        except:
            pass

        if os.access(tmpfile,0):
            os.remove(tmpfile)
        if group is not None:
            shutil.rmtree(group)
        return res

    def test(self):
        self.__process('dir', 3, False, 'e:\\7\\Video\\1.ts')


# tool = FFmpegTool(1)
# src = u'e:\\7\\Album\\Beyonc\xe9\\Lemonade/01 Pray You Catch Me.mp4'
# # s = src.encode(sys.getfilesystemencoding())
# # short_path = win32api.GetShortPathName(src)
# desc = u'e:\\7\\Album\\Beyonc\xe9\\Lemonade/01 Pray You Catch Me.m4a'
# tool.covertFile(src, desc)
