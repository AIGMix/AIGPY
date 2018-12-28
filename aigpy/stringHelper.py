"""
#Func    :   判断字符串是否单纯为中文
#Param   :   word               字符串
#Param   :   checkPunctuation   检查标点符号
#Return  :   True/False 
"""
def isChinese(word, checkPunctuation = False):
    punctuationStr = '，。！？【】（）％＃＠＆１２３４５６７８９０：'
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
        if checkPunctuation and punctuationStr.find(ch) != -1:
            return True
    return False

"""
#Func    :   将中文标点字符转为英文
#Param   :   word   字符串
#Return  :   字符串
"""
def converPunctuationToEnglish(word):
    table = {ord(f): ord(t) for f, t in zip(
        u'，。！？【】（）％＃＠＆１２３４５６７８９０：',
        u',.!?[]()%#@&1234567890:')}
    ret = word.translate(table)
    return ret

"""
#Func    :   字符串对齐
#Param   :   string     字符串
#Param   :   num        对齐宽度
#Param   :   isLeft     是否左对齐
#Return  :   字符串
"""
def align(string, num, isLeft=True):
    len = 0
    for c in string:
        len += 1
        if isChinese(c, True):
            len += 1
    if len >= num:
        return string
    appendStr = ""
    while num - len > 0:
        appendStr += " "
        num -= 1
    if isLeft:
        return string + appendStr
    else:
        return appendStr + string
