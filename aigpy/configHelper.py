#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   configHelper.py
@Time    :   2018/12/17
@Author  :   Yaron Huang 
@Version :   1.0
@Contact :   yaronhuang@qq.com
@Desc    :   
'''
import os
import configparser

def Count(fileName, section=None):
    try:
        ret = 0
        cf  = configparser.ConfigParser()
        cf.read(fileName)
        if section == None:
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
    try:
        cf = configparser.ConfigParser()
        cf.read(fileName)
        return cf.sections()
    except:
        return None

def GetValue(section, key, default, fileName):
    cf = configparser.ConfigParser()
    cf.read(fileName)
    if cf.has_section(section) == False:
        return default

    for item in cf[section]:
        if item == key:
            str = cf.get(section, key)
            return str
    return default

def SetValue(section, key, value, fileName):
    if os.access(fileName, 0) == False:
        fp = open(fileName, "w")
        fp.close()

    cf = configparser.ConfigParser()
    cf.read(fileName)
    if cf.has_section(section) == False:
        cf[section] = {}

    cf[section][key] = value
    with open(fileName, "w") as f:
        cf.write(f)
