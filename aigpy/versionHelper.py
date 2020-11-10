#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import aigpy.configHelper as ConfigHelper


def cmpVersion(ver1, ver2):
    array1 = ver1.split('.')
    array2 = ver2.split('.')
    iIndex = 0
    for obj in array1:
        if len(array2) <= iIndex:
            break
        if obj > array2[iIndex]:
            return 1
        if obj < array2[iIndex]:
            return -1
        iIndex = iIndex + 1
    return 0


class VersionFile(object):
    def __init__(self, path=None):
        self.version      = None
        self.mainFile     = None
        self.elseFileList = []
        self.isZip        = 0
        self.zipFile      = ''
        if path != None:
            self.readFile(path)

    def saveFile(self, path):
        if path is None or self.version is None or self.mainFile is None:
            return False
        if self.isZip != 0 and self.zipFile == '':
            return False

        check = ConfigHelper.SetValue('common', 'version',  self.version, path)
        check = ConfigHelper.SetValue('common', 'mainfile', self.mainFile, path)
        if check is False:
            return False
        check = ConfigHelper.SetValue('common', 'iszip',  self.isZip, path)
        check = ConfigHelper.SetValue('common', 'zipfile',  self.isZip, path)

        if self.elseFileList is None or len(self.elseFileList) == 0:
            return True
        ConfigHelper.SetValue('common', 'elsenum', len(self.elseFileList), path)
        index = 0
        for item in self.elseFileList:
            ConfigHelper.SetValue('common', 'else' + index, item, path)
            index = index + 1
        return True

    def readFile(self, path):
        if path is None:
            return False
        ver = ConfigHelper.GetValue('common', 'version', '', path)
        mainFile = ConfigHelper.GetValue('common', 'mainfile', '', path)
        if ver == '' or mainFile == '':
            return False

        isZip = ConfigHelper.GetValue('common', 'iszip', 0, path)
        isZip = int(isZip)
        zipFile = ConfigHelper.GetValue('common', 'zipfile', '', path)
        if isZip != 0 or zipFile == '':
            return False

        elseNum = ConfigHelper.GetValue('common', 'elsenum', 0, path)
        elseNum = int(elseNum)
        elseList = []
        index = 0
        if elseNum > 0:
            obj = ConfigHelper.GetValue('common', 'else' + index, '', path)
            index = index + 1
            elseList.append(obj)

        self.version = ver
        self.mainFile = mainFile
        self.elseFileList = elseList
        self.isZip = isZip
        self.zipFile = zipFile
        return True



