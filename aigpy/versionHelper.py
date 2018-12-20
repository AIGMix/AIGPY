#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   versionHelper.py
@Time    :   2018/12/20
@Author  :   Yaron Huang 
@Version :   1.0
@Contact :   yaronhuang@qq.com
@Desc    :   
'''

import os
import platform

def getVersion(in_filepath):
    try:
        if os.path.isfile(in_filepath) == False:
            return ""
        if os.path.exists(in_filepath) == False:
            return ""
        
        # get system
        sysName = platform.system()
        if sysName == "Windows":
            import win32api
            info    = win32api.GetFileVersionInfo(in_filepath, os.sep)
            ms      = info['FileVersionMS']
            ls      = info['FileVersionLS']
            version = '%d.%d.%d.%04d' % (win32api.HIWORD(ms), win32api.LOWORD(ms), win32api.HIWORD(ls), win32api.LOWORD(ls))
            return version
        if sysName == "Linux":
            return ""
        return ""
    except:
        return ""
