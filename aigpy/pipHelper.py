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
    ret = getInfo(projectName)
    if ret == None:
        return None
    return ret['info']['version']

def getVersionList(projectName):
    ret = getInfo(projectName)
    if ret == None:
        return None
    return ret['releases']

