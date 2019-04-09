#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   stringHelper.py
@Time    :   2019/03/11
@Author  :   Yaron Huang 
@Version :   1.0
@Contact :   yaronhuang@qq.com
@Desc    :   
'''



def isChinese(word, checkPunctuation = False):
    """
    #Func    :   判断字符串是否单纯为中文           
    #Param   :   word               字符串          
    #Param   :   checkPunctuation   检查标点符号            
    #Return  :   True/False 
    """
    punctuationStr = '，。！？【】（）％＃＠＆１２３４５６７８９０：'
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
        if checkPunctuation and punctuationStr.find(ch) != -1:
            return True
    return False


def converPunctuationToEnglish(word):
    """
    #Func    :   将中文标点字符转为英文         
    #Param   :   word   字符串          
    #Return  :   字符串         
    """
    table = {ord(f): ord(t) for f, t in zip(
        u'，。！？【】（）％＃＠＆１２３４５６７８９０：',
        u',.!?[]()%#@&1234567890:')}
    ret = word.translate(table)
    return ret


def align(string, num, isLeft=True):
    """
    #Func    :   字符串对齐         
    #Param   :   string     字符串          
    #Param   :   num        对齐宽度            
    #Param   :   isLeft     是否左对齐          
    #Return  :   字符串         
    """
    leng = 0
    for c in string:
        leng += 1
        if isChinese(c, True):
            leng += 1
    if leng >= num:
        return string
    appendStr = ""
    while num - leng > 0:
        appendStr += " "
        num -= 1
    if isLeft:
        return string + appendStr
    else:
        return appendStr + string

