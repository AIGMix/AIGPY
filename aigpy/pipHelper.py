#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   pipHelper.py
@Time    :   2019/03/11
@Author  :   Yaronzz 
@Version :   2.0
@Contact :   yaronhuang@foxmail.com
@Desc    :   pip server tool
'''

import aigpy.netHelper as netHelper

def getInfo(projectName):
    """Get project information from pypi
    - Return: json or None                              
    """
    url = 'https://pypi.org/pypi/' + projectName + '/json'
    ret = netHelper.downloadJson(url,None)
    return ret
    

def getLastVersion(projectName):
    """Get project version from pypi
    - Return: str or None                              
    """
    try:
        ret = getInfo(projectName)
        if ret is None:
            return None
        return ret['info']['version']
    except:
        return None


def getVersionList(projectName):
    """Get project all versions from pypi
    - Return: json or None                              
    """
    try:
        ret = getInfo(projectName)
        if ret is None:
            return None
        return ret['releases']
    except:
        return None


