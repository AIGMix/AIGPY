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

def isChinese(word, checkPunctuation=False):
    punctuationStr = '，。！？【】（）％＃＠＆１２３４５６７８９０：'
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
        if checkPunctuation and punctuationStr.find(ch) != -1:
            return True
    return False


def converPunctuationToEnglish(word):
    table = {ord(f): ord(t) for f, t in zip(
        u'，。！？【】（）％＃＠＆１２３４５６７８９０：',
        u',.!?[]()%#@&1234567890:')}
    ret = word.translate(table)
    return ret


def align(string, num, isLeft=True):
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
