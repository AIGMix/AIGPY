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
import ctypes
import platform
from enum import Enum


def isInputYes(inputstr):
    """
    #Func    :   输入的字符串是否为yes      
    #Param   :   inputstr   [in] 输入串     
    #Return  :   True/False         
    """
    if inputstr is None:
        return False
    inputstr = str(inputstr).lower()
    if inputstr == 'yes' or inputstr == 'y':
        return True
    return False

def myinput(desc):
    """
    #Func    :   输入优化-支持python2.x/3.x    
    #Param   :   desc  [in] 描述  
    #Return  :   输入的参数
    """
    v = sys.version_info
    if v[0] > 2:
        return input(desc)
    else:
        return raw_input(desc)

def myinputInt(desc, default):
    """
    #Func    :   输入整型优化-支持python2.x/3.x 
    #Param   :   desc       [in] 描述      
    #Param   :   default    [in] 默认的整型数     
    #Return  :   输入的整型数         
    """
    try:
        stri = myinput(desc)
        ret  = int(stri)
        return ret
    except:
        return default

def myinputFloat(desc, default):
    """
    #Func    :   输入浮点数优化-支持python2.x/3.x 
    #Param   :   desc       [in] 描述      
    #Param   :   default    [in] 默认的浮点数     
    #Return  :   输入的浮点数         
    """
    try:
        stri = myinput(desc)
        ret  = float(stri)
        return ret
    except:
        return default


def findInArgv(stri):
    """
    #Func    :   mian参列表中查找第一个有此子串的项      
    #Param   :   stri    [in] 子串       
    #Return  :   None/子项    
    """
    if sys.argv == None or len(sys.argv) == 0:
        return None
    
    for item in sys.argv:
        if item == sys.argv[0]:
            continue
        if item.find(stri) >= 0:
            return item
    return None

def converArgvToStr(array):
    """
    #Func    :   将列表转成main参字符串     
    #Param   :   list   [in] 项列表     
    #Return  :   字符串         
    """
    stri = ''
    for item in array:
        if stri != '':
            stri = stri + ' '
        stri = stri + '"' + item + '"'
    return stri


class TextColor(Enum):
    """
    #Func    :   前景颜色
    """
    if platform.system() == 'Windows':
        Black   = 0x00
        Blue    = 0x09
        Green   = 0x0a
        Red     = 0x0c
        Yellow  = 0x0e
        White   = 0x0f
    else:
        Black  = 30
        Blue   = 34
        Green  = 32
        Red    = 31
        Yellow = 33
        White  = 37

class BackGroundColor(Enum):
    """
    #Func    :   背景颜色
    """
    if platform.system() == 'Windows':
        Black   = 0x00
        Blue    = 0x90
        Green   = 0xa0
        Red     = 0xc0
        Yellow  = 0xe0
        White   = 0xf0
    else:
        Black  = 40
        Blue   = 44
        Green  = 42
        Red    = 41
        Yellow = 43
        White  = 47
class WinCmdHandleID(Enum): 
    """
    #Func    :   Windows的输入、输出、错误输出的句柄ID
    """
    Input  = -10
    Output = -11
    Error  = -12

def myprint(desc,textColor=None,backgroundColor=None):
    """
    #Func    :   输出       
    #Param   :   desc               [in] 信息       
    #Param   :   textColor          [in] 前景颜色       
    #Param   :   backgroundColor    [in] 背景颜色       
    #Return  :   None 
    """
    if textColor is None and backgroundColor is None:
        sys.stdout.write(desc)
    else:
        if platform.system() == 'Windows':
            color = 0
            if textColor is not None:
                color = color | textColor.value
            if backgroundColor is not None:
                color = color | backgroundColor.value
            #获取输出句柄,修改颜色
            handle = ctypes.windll.kernel32.GetStdHandle(WinCmdHandleID.Output.value)
            ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
            sys.stdout.write(desc)
            #设置回原来的颜色
            value = TextColor.Red.value | TextColor.Green.value | TextColor.Blue.value
            ctypes.windll.kernel32.SetConsoleTextAttribute(handle, value)
        else:
            color = ''
            if textColor is not None:
                color = str(textColor.value)
            if backgroundColor is not None:
                if color != '':
                    color = color +';'
                color = color + str(backgroundColor.value)
            color = color + 'm'
            sys.stdout.write("\033[" + color + str(desc) + "\033[0m")

def showTable(columns, rows, colsColor=None, rowsColor=None):
    """
    #Func    :   显示表格       
    #Param   :   columns    [in] 列名数组       
    #Param   :   rows       [in] 行值数组-二维数组             
    #Param   :   colsColor  [in] 列名颜色                  
    #Param   :   rowsColor  [in] 行颜色                       
    #Return  :   True/False 
    """
    try:
        widths = []
        for item in columns:
            name = str(item)   
            widths.append(len(name))
        
        for rObj in rows:
            index = 0
            for item in rObj:
                if len(item) > widths[index]:
                    widths[index] = len(item)
                index = index + 1
                if len(widths) <= index:
                    break
        
        boardstr = '-'
        for item in widths:
            for i in range(item + 2 + 1):
                boardstr = boardstr + '-'

        print(boardstr)
        index = 0
        for item in columns:
            item = item.center(widths[index] + 2)
            print('|', end='')
            myprint(item, colsColor)
            index = index + 1
            if len(widths) <= index:
                break
        print('|')
        print(boardstr)
        for rObj in rows:
            index = 0
            for item in rObj:
                item = item.center(widths[index] + 2)
                print('|',end='')
                myprint(item, rowsColor)
                index = index + 1
                if len(widths) <= index:
                    break
            print('|')
        print(boardstr)
        return True
    except:
        return False
