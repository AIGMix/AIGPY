#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   cmdHelper.py
@Time    :   2019/02/27
@Author  :   Yaron Huang 
@Version :   1.0
@Contact :   yaronhuang@qq.com
@Desc    :   
'''

import sys

# Compatible with python 2.x version
def myinput(desc):
    v = sys.version_info
    if v[0] > 2:
        return input(desc)
    else:
        return raw_input(desc)

def findInArgv(str):
    if sys.argv == None or len(sys.argv) == 0:
        return None
    
    for item in sys.argv:
        if item == sys.argv[0]:
            continue
        if item.find(str) >= 0:
            return item
    return None

def converArgvToStr(list):
    str = ''
    for item in list:
        if str != '':
            str = str + ' '
        str = str + '"' + item + '"'
    return str