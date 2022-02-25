#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  downloadHelper.py
@Date    :  2021/02/07
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :  
"""
import abc
import requests

from aigpy.LockHelper import RWLock
from aigpy.fileHelper import createEmptyFile
from aigpy.memoryHelper import convert, Unit, unitFix
from aigpy.progressHelper import ProgressTool
from aigpy.threadHelper import ThreadTool


class __Part__(object):
    def __init__(self, url: str, requestOffset: int, requestLength: int, fileOffset: int):
        self.url = url
        self.requestOffset = requestOffset
        self.requestLength = requestLength
        self.fileOffset = fileOffset


class UserProgress(metaclass=abc.ABCMeta):
    def __init__(self):
        self.maxNum = 100
        self.curNum = 0
        
    def setMaxNum(self, maxNum: int):
        self.maxNum = maxNum
        self.updateMaxNum()

    def addCurNum(self, num: int):
        self.curNum += num
        self.updateCurNum()
    
    def setCurNum(self, num: int):
        self.curNum = num
        self.updateCurNum()
        
    @abc.abstractmethod
    def updateCurNum(self):
        pass
    
    @abc.abstractmethod
    def updateMaxNum(self):
        pass


def __downloadPartFile__(part: __Part__, parent, progress, unit, retry=3):
    error = None
    while retry > 0:
        retry -= 1
        try:
            rang = 'bytes=%s-%s' % (part.requestOffset, part.requestOffset + part.requestLength - 1)
            headers = {'Range': rang}

            res = requests.get(part.url, headers=headers, timeout=(5, 30), proxies=parent.proxies)
            res.raise_for_status()
        except Exception as e:
            error = e
            continue

        content = res.content

        parent.lock.write_acquire()
        try:
            with open(parent.filePath, 'rb+') as f:
                f.seek(part.fileOffset)
                f.write(content)
            if progress is not None:
                progress.addCurCount(convert(part.requestLength, Unit.BYTE, unit))
            if parent.userProgress is not None:
                parent.userProgress.addCurNum(part.requestLength)
            parent.curSize += part.requestLength
        except Exception as e:
            error = e
            parent.lock.write_release()
            continue
        parent.lock.write_release()
        
        return True, ""
    return False, error


class DownloadTool(object):
    def __init__(self, filePath: str, fileUrls: list, proxies: dict = None):
        self.filePath = filePath
        self.fileUrls = fileUrls
        self.proxies = proxies
        self.partSize = 1048576
        
        self.maxSize = 0
        self.curSize = 0
        
        self.userProgress = None
        self.lock = RWLock()
    
    def __getSize__(self, url):
        ret = requests.head(url, proxies=self.proxies)
        if 'Content-Length' in ret.headers:
            return int(ret.headers['Content-Length'])
        return -1

    def __getUrlsSize__(self, urls):
        totalSize = 0
        array = []
        for item in urls:
            size = self.__getSize__(item)
            totalSize += size
            if size < 0:
                return -1, []
            array.append(size)
        return totalSize, array

    def __getOneUrlParts__(self, url):
        fileSize = self.__getSize__(url)
        if fileSize <= 0:
            return 0, [], "Get file size failed."

        offset = 0
        parts = []
        length = fileSize
        while length > 0:
            if length > self.partSize:
                bf = __Part__(url, offset, self.partSize, offset)
            else:
                bf = __Part__(url, offset, length, offset)
            parts.append(bf)
            offset += self.partSize
            length -= self.partSize
        return fileSize, parts, ""

    def __getMoreUrlsParts__(self, urls):
        fileSize, urlSizes = self.__getUrlsSize__(urls)
        if fileSize <= 0:
            return 0, [], "Get some file sizes failed."

        parts = []
        offset = 0
        for i, url in enumerate(urls):
            parts.append(__Part__(url, 0, urlSizes[i], offset))
            offset += urlSizes[i]
        return fileSize, parts, ""

    def setUserProgress(self, progress):
        self.userProgress = progress
        
    def setPartSize(self, size: int):
        self.partSize = size
    
    def start(self, showProgress: bool = False, threadNum: int = 10) -> (bool, str):
        size = len(self.fileUrls)
        if size == 1:
            fileSize, parts, msg = self.__getOneUrlParts__(self.fileUrls[0])
        elif size > 1:
            fileSize, parts, msg = self.__getMoreUrlsParts__(self.fileUrls)
        else:
            return False, "Urls is empty."

        if msg != "":
            return False, msg
        
        self.maxSize = fileSize

        try:
            check = createEmptyFile(self.filePath, fileSize)
            if not check:
                return False, "Create file failed."

            if self.userProgress is not None:
                self.userProgress.setMaxNum(fileSize)
                
            # thread
            threads = ThreadTool(threadNum)
            fileSize, unit = unitFix(fileSize, Unit.BYTE, Unit.MB)

            # Progress
            progress = None
            if showProgress:
                progress = ProgressTool(fileSize, 15, unit=unit.name)

            for item in parts:
                threads.start(__downloadPartFile__, item, self,progress, unit, 3)
            results = threads.waitAll()
            threads.close()

            for item in results:
                if item[0] is False:
                    return False, "Some parts download failed." + item[1]
            return True, ""
        except Exception as e:
            return False, str(e)


