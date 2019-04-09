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
    """
    #Func    :   获取pip上项目的信息                                                              
    #Param   :   projectName      [in] 项目名                                                     
    #Return  :   json or None                              
    """
    url = 'https://pypi.org/pypi/' + projectName + '/json'
    ret = netHelper.downloadJson(url,None)
    return ret
    
def getLastVersion(projectName):
    """
    #Func    :   获取pip上项目的最新的版本号                                                                      
    #Param   :   projectName      [in] 项目名                                                     
    #Return  :   Err:None                               
    """
    try:
        ret = getInfo(projectName)
        if ret is None:
            return None
        return ret['info']['version']
    except:
        return None

def getVersionList(projectName):
    """
    #Func    :   获取pip上项目的全部版本信息                                                                 
    #Param   :   projectName      [in] 项目名                                                     
    #Return  :   数组 or None                               
    """
    try:
        ret = getInfo(projectName)
        if ret is None:
            return None
        return ret['releases']
    except:
        return None
