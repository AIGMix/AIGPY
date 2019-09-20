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
    """Get para number"""
    try:
        ret = 0
        cf = configparser.ConfigParser()
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
    """Get groups"""
    try:
        cf = configparser.ConfigParser()
        cf.read(fileName)
        return cf.sections()
    except:
        return None


def GetValue(section, key, default, fileName):
    try:
        cf = configparser.ConfigParser()
        cf.read(fileName)
        if not cf.has_section(section):
            return default
        
        if key in cf[section]:
            default = cf.get(section, key)
        return default
    except:
        return default

def SetValue(section, key, value, fileName):
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


def ParseNoEqual(fileName):
    ret = {}
    try:
        fd  = open(fileName, 'r')
        arr = fd.readlines()
        group = None
        for item in arr:
            item = item.strip()
            if len(item) <= 0:
                continue
            if item[0] == '#':
                continue
            elif item[0] == '[' and item[len(item) - 1] == ']':
                group = item[1:len(item) - 1]
                ret[group] = []
            elif group is None:
                continue
            else:
                ret[group].append(item)
        return ret     
    except:
        return ret

