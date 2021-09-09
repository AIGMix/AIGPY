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


def __downloadPartFile__(part: __Part__, fileName: str, lock, progress, unit, retry=3, proxies=None):
    error = None
    while retry > 0:
        retry -= 1
        try:
            rang = 'bytes=%s-%s' % (part.requestOffset, part.requestOffset + part.requestLength - 1)
            headers = {'Range': rang}

            res = requests.get(part.url, headers=headers, timeout=(5, 30), proxies=proxies)
            res.raise_for_status()
        except Exception as e:
            error = e
            continue

        lock.write_acquire()
        try:
            with open(fileName, 'rb+') as f:
                f.seek(part.fileOffset)
                f.write(res.content)
            if progress is not None:
                progress.addCurCount(convert(part.requestLength, Unit.BYTE, unit))
        except Exception as e:
            error = e
            lock.write_release()
            continue

        lock.write_release()
        return True, ""
    return False, error


class DownloadTool(object):
    def __init__(self, filePath: str, fileUrls: list, proxies: dict = None):
        self.filePath = filePath
        self.fileUrls = fileUrls
        self.proxies = proxies
        self.__partSize__ = 1048576

    def __getSize__(self, url):
        ret = requests.get(url, proxies=self.proxies)
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

    def __getOneUrlParts__(self, url, partSize) -> (int, list, str):
        fileSize = self.__getSize__(url)
        if fileSize <= 0:
            return 0, [], "Get file size failed."

        offset = 0
        parts = []
        length = fileSize
        while length > 0:
            if length > partSize:
                bf = __Part__(url, offset, partSize, offset)
            else:
                bf = __Part__(url, offset, length, offset)
            parts.append(bf)
            offset += partSize
            length -= partSize
        return fileSize, parts, ""

    def __getMoreUrlsParts__(self, urls) -> (int, list, str):
        fileSize, urlSizes = self.__getUrlsSize__(urls)
        if fileSize <= 0:
            return 0, [], "Get some file sizes failed."

        parts = []
        offset = 0
        for i, url in enumerate(urls):
            parts.append(__Part__(url, 0, urlSizes[i], offset))
            offset += urlSizes[i]
        return fileSize, parts, ""

    def start(self, showProgress: bool = False, threadNum: int = 10) -> (bool, str):
        size = len(self.fileUrls)
        if size == 1:
            fileSize, parts, msg = self.__getOneUrlParts__(self.fileUrls[0], self.__partSize__)
        elif size > 1:
            fileSize, parts, msg = self.__getMoreUrlsParts__(self.fileUrls)
        else:
            return False, "Urls is empty."

        if msg != "":
            return False, msg

        try:
            check = createEmptyFile(self.filePath, fileSize)
            if not check:
                return False, "Create file failed."

            # thread
            threads = ThreadTool(threadNum)
            fileSize, unit = unitFix(fileSize, Unit.BYTE, Unit.MB)

            # Progress
            progress = None
            if showProgress:
                progress = ProgressTool(fileSize, 15, unit=unit.name)

            lock = RWLock()
            for item in parts:
                threads.start(__downloadPartFile__, item, self.filePath, lock, progress, unit, 3, self.proxies)
            results = threads.waitAll()
            threads.close()

            for item in results:
                if item[0] is False:
                    return False, "Some parts download failed." + item[1]
            return True, ""
        except Exception as e:
            return False, str(e)

    def setPartSize(self, size: int):
        self.__partSize__ = size
