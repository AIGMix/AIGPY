#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   cmdHelper.py
@Time    :   2019/02/27
@Author  :   Yaronzz 
@Version :   2.1
@Contact :   yaronhuang@foxmail.com
@Desc    :   
'''

import sys
from enum import Enum
from colorama import init

init(autoreset=True)

def isInputYes(string) -> bool:
    if string is None:
        return False
    string = str(string).lower()
    if string == 'yes' or string == 'y':
        return True
    return False


def inputInt(desc: str, default: int) -> int:
    try:
        string = input(desc)
        ret = int(string)
        return ret
    except:
        return default


def inputFloat(desc: str, default: int) -> float:
    try:
        string = input(desc)
        ret = float(string)
        return ret
    except:
        return default


def printNoEnter(desc: str):
    sys.stdout.write(desc)


def findInArgv(string):
    if sys.argv is None or len(sys.argv) <= 0:
        return None
    for item in sys.argv:
        if item == sys.argv[0]:
            continue
        if item.find(string) >= 0:
            return item
    return None


def converArgvToStr(array):
    string = ''
    for item in array:
        if string != '':
            string += ' '
        string = string + '"' + item + '"'
    return string


class TextColor(Enum):
    """Font color"""
    Black = 30
    Blue = 34
    Green = 32
    Red = 31
    Yellow = 33
    White = 37


class BackGroundColor(Enum):
    Black = 40
    Blue = 44
    Green = 42
    Red = 41
    Yellow = 43
    White = 47



def green(text):
    return "\033[" + str(TextColor.Green.value) + 'm' + str(text) + "\033[0m"
def blue(text):
    return "\033[" + str(TextColor.Blue.value) + 'm' + str(text) + "\033[0m"
def red(text):
    return "\033[" + str(TextColor.Red.value) + 'm' + str(text) + "\033[0m"
def yellow(text):
    return "\033[" + str(TextColor.Yellow.value) + 'm' + str(text) + "\033[0m"



def myprint(desc, textColor=None, bgColor=None):
    if textColor is None and bgColor is None:
        sys.stdout.write(desc)
    else:
        color = ''
        if textColor is not None:
            color = str(textColor.value)
        if bgColor is not None:
            if color != '':
                color = color + ';'
            color = color + str(bgColor.value)
        color = color + 'm'
        sys.stdout.write("\033[" + color + str(desc) + "\033[0m")
