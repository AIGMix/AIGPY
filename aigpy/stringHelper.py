#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   stringHelper.py
@Time    :   2019/03/11
@Author  :   Yaronzz 
@Version :   2.0
@Contact :   yaronhuang@foxmail.com
@Desc    :   
'''


def isNull(word):
    if word is None or word == "":
        return True
    return False


def isNotNull(word):
    if isNull(word):
        return False
    return True


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


def getSubOnlyStart(string, start):
    if start not in string:
        return ""
    index = string.index(start)
    return string[index + len(start):]


def getSubOnlyEnd(string, end):
    if end not in string:
        return ""
    index = string.index(end)
    return string[0:index]


def getSub(string, start=None, end=None):
    if start is None and end is None:
        return string
    if end is None:
        return getSubOnlyStart(string, start)
    if start is None:
        return getSubOnlyEnd(string, end)

    string = getSubOnlyStart(string, start)
    if string == "":
        return ""

    ret = getSubOnlyEnd(string, end)
    if ret == "":
        ret = string
    return ret



