#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   configHelper.py
@Time    :   2018/12/17
@Author  :   Yaron Huang 
@Version :   1.0
@Contact :   yaronhuang@qq.com
@Desc    :   Config Tool
'''
import os
import configparser

def Count(fileName, section=None):
    """
    #Func    :   获取文件中参数的数量       
    #Param   :   fileName [in]  文件名          
    #Param   :   section  [in]  组名                  
    #Return  :   int型
    """
    try:
        ret = 0
        cf  = configparser.ConfigParser()
        cf.read(fileName)
        if section is None:
            seclist = cf.sections()
            for sec in seclist:
                oplist = cf.options(sec)
                ret    = ret + len(oplist)
        elif cf.has_section(section):
            ret = len(cf[section])
            
        return ret
    except:
        return 0

def Sections(fileName):
    """
    #Func    :   获取文件中小组列表句柄           
    #Param   :   fileName [in] 文件名       
    #Return  :   Err:None        
    """
    try:
        cf = configparser.ConfigParser()
        cf.read(fileName)
        return cf.sections()
    except:
        return None

def GetValue(section, key, default, fileName):
    """
    #Func    :   获取参数值          
    #Param   :   section    [in] 小组名     
    #Param   :   key        [in] 参数名     
    #Param   :   default    [in] 默认值     
    #Param   :   fileName   [in] 文件名     
    """
    try:
        cf = configparser.ConfigParser()
        cf.read(fileName)
        if cf.has_section(section) == False:
            return default

        for item in cf[section]:
            if item == key:
                stri = cf.get(section, key)
                return stri
        return default
    except:
        return default

def SetValue(section, key, value, fileName):
    """
    #Func    :   设置值             
    #Param   :   section    [in] 小组名     
    #Param   :   key        [in] 参数名     
    #Param   :   value      [in] 参数值      
    #Param   :   fileName   [in] 文件名         
    #Return  :   True/False 
    """
    try:
        if os.access(fileName, 0) is False:
            fp = open(fileName, "w")
            fp.close()

        cf = configparser.ConfigParser()
        cf.read(fileName)
        if cf.has_section(section) is False:
            cf[section] = {}

        cf[section][key] = value
        with open(fileName, "w") as f:
            cf.write(f)
        return True
    except:
        return False

