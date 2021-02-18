#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :  convertHelper.py
@Date    :  2020/11/16
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :  
'''

from enum import Enum


class MemoryUnit(Enum):
    GB = 0
    MB = 1
    KB = 2
    BYTE = 3


def convertMemoryUnit(num: float, srcUnit: MemoryUnit, desUnit: MemoryUnit) -> float:
    """Convert memory unit, support gb/mb/kb/byte

    Args:
        num (float): value
        srcUnit (MemoryUnit): Original unit
        desUnit (MemoryUnit): Target unit
    """
    if srcUnit == desUnit:
        return num

    try:
        num = float(num)
        if num == 0:
            return 0
        srcIndex = srcUnit.value
        desIndex = desUnit.value
        diff = abs(srcIndex - desIndex)

        while diff != 0:
            if srcIndex < desIndex:
                num = num * 1024
            else:
                num = num / 1024
            diff -= 1

        return num
    except ValueError:
        return 0


def convertMemoryUnitAuto(num: float, unit: MemoryUnit, maxUnit: MemoryUnit) -> (float, MemoryUnit):
    """Automatic conversion to appropriate units

    Args:
        num (float): value
        MemoryUnit (MemoryUnit): Original unit

    Returns:
        [float, MemoryUnit]: target value and unit
    """
    try:
        num = float(num)
        if num == 0:
            return 0, unit

        index = unit.value
        while index > maxUnit.value:
            newNum = num / 1024
            if newNum < 1:
                break
            num = newNum
            index -= 1

        return num, MemoryUnit(index)
    except ValueError:
        return 0, MemoryUnit.BYTE


def getMemoryUnitString(num: float, unit: MemoryUnit) -> str:
    """Convert the unit to string, eg: num(2653)unit(MB) -> '2.59 GB'

    Args:
        num (float): value
        unit (MemoryUnit): Original unit

    Returns:
        [string]: target string, keep two decimal places
    """
    value, newUnit = convertMemoryUnitAuto(num, unit, MemoryUnit.GB)
    string = str(round(value, 2)) + ' ' + newUnit.name
    return string
