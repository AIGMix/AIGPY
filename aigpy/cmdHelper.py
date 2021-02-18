#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   cmdHelper.py
@Time    :   2019/02/27
@Author  :   Yaronzz 
@Version :   2.2
@Contact :   yaronhuang@foxmail.com
@Desc    :   
'''
import os
import sys
from enum import Enum
from colorama import init
from aigpy.pathHelper import mkdirs

init(autoreset=True)


def isInputYes(string: str) -> bool:
    """Check the input string == yes|y|Yes|Y"""
    if string is not None:
        if str(string).lower() in ['yes', 'y']:
            return True
    return False


def inputInt(desc: str, default: int) -> int:
    try:
        string = input(desc)
        return int(string)
    except ValueError:
        return default


def inputFloat(desc: str, default: int) -> float:
    try:
        string = input(desc)
        return float(string)
    except ValueError:
        return default


def inputPath(desc: str, ignore: str = "") -> str:
    """
    Input path

    return:
    - path: existed or mkdirs success
    """
    path = input(desc)
    if path == ignore:
        return ignore
    if os.path.isdir(path) or mkdirs(path):
        return path
    return ""


def inputLimit(desc: str, limit: list) -> str:
    """
    Input limit

    return:
    - path: input string in limit list
    - none
    """
    string = input(desc)
    if string in limit:
        return string
    return None


def printW(desc: str, wrap: bool = True):
    """Print desc width wrap or not"""
    if not wrap:
        sys.stdout.write(desc)
    else:
        print(desc)


def isInArgv(string):
    array = sys.argv
    if array is None or len(array) <= 0:
        return False

    array.pop(0)
    if string in array:
        return True
    return False


class TextColor(Enum):
    """Font color"""
    Black = 30
    Blue = 34
    Green = 32
    Red = 31
    Yellow = 33
    White = 37


class BackgroundColor(Enum):
    Black = 40
    Blue = 44
    Green = 42
    Red = 41
    Yellow = 43
    White = 47


def __getColorString__(color: TextColor, bgColor: BackgroundColor, text: str):
    if color is None and bgColor is None:
        return text

    array = []
    if color is not None:
        array.append(str(color.value))
    if bgColor is not None:
        array.append(str(bgColor.value))
    return "\033[" + ';'.join(array) + 'm' + str(text) + "\033[0m"


def green(text):
    return __getColorString__(TextColor.Green, None, text)


def blue(text):
    return __getColorString__(TextColor.Blue, None, text)


def red(text):
    return __getColorString__(TextColor.Red, None, text)


def yellow(text):
    return __getColorString__(TextColor.Yellow, None, text)


def colorPrint(desc: str, textColor: TextColor = None, bgColor: BackgroundColor = None):
    """Print color string
    
    - textColor (TextColor): font color
    - bgColor (BackgroundColor): background color
    
    """
    string = __getColorString__(textColor, bgColor, desc)
    printW(string, False)
