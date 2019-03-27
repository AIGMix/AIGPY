#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   pipHelper.py
@Time    :   2019/03/11
@Author  :   Yaron Huang 
@Version :   1.0
@Contact :   yaronhuang@qq.com
@Desc    :   pip server tool
'''

import aigpy.netHelper as netHelper

def getInfo(projectName):
    url = 'https://pypi.org/pypi/' + projectName + '/json'
    ret = netHelper.downloadJson(url,None)
    return ret
    
def getLastVersion(projectName):
    try:
        ret = getInfo(projectName)
        if ret == None:
            return None
        return ret['info']['version']
    except:
        return None

def getVersionList(projectName):
    try:
        ret = getInfo(projectName)
        if ret == None:
            return None
        return ret['releases']
    except:
        return None
