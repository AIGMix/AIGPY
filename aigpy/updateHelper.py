#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   updateHelper.py
@Time    :   2018/12/20
@Author  :   Yaron Huang 
@Version :   1.0
@Contact :   yaronhuang@qq.com
@Desc    :   
'''
import os
import sys

import aigpy.netHelper as netHelper
import aigpy.pathHelper as pathHelper
import aigpy.systemHelper as systemHelper
import aigpy.versionHelper as versionHelper

class updateTool(object):
    def __init__(self, in__file__):
        self._file_  = in__file__
        self.tmpName = "#AigpyNewVersion#"
        self.curPath = systemHelper.getOwnPath(in__file__)
        self.tmpPath = self.curPath + '\\' + self.tmpName
        return

    def getOwnVersion(self):
        return versionHelper.getVersion(self._file_)

    def downloadFiles(self, in_url, in_aFilePaths):
        # 新建临时目录
        check = pathHelper.remove(self.tmpPath)
        check = pathHelper.mkdirs(self.tmpPath)

        # 下载新版本文件到临时目录
        for item in in_aFilePaths:
            urlpath = in_url + '\\' + item
            topath = self.tmpPath + '\\' + item
            if netHelper.downloadFile(urlpath, topath) == False:
                return False
        return True

    # def start(self):
    #     try:
    #         if systemHelper.isWindows() == False:
    #             return False

    #         path = self.curPath + "\\AigpyUpdate.bat"
    #         with open(path, 'w') as fd: 
    #             TempList  = "@echo off\n"  # 关闭bat脚本的输出
    #             TempList += "if not exist " + self.tmpPath + " exit \n"  # 新文件不存在, 退出脚本执行
    #             TempList += "sleep 3\n"  # 3秒后删除旧程序（3秒后程序已运行结束，不延时的话，会提示被占用，无法删除）
    #             TempList += "del " + os.path.realpath(sys.argv[0]) + "\n"  # 删除当前文件
    #             TempList += "start " + exe_name  # 启动新程序
    #             b.write(TempList)
    #             b.close()
    #             subprocess.Popen("upgrade.bat")
    #             sys.exit()  # 进行升级，退出此程序
    #     except :
    #         return False