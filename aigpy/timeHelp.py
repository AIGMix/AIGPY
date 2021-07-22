#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  time.py
@Date    :  2021/05/25
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :  
"""


def strToSecond(timeStr: str, splitC: str = ":") -> int:
    array = timeStr.split(splitC)
    if len(array) == 1:
        return int(array[0])
    elif len(array) == 2:
        return int(array[0]) * 60 + int(array[1])
    elif len(array) == 3:
        return int(array[0]) * 3600 + int(array[1]) * 60 + int(array[2])
    return 0
