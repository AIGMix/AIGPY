#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  memoryHelper.py
@Date    :  2021/8/4
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :
"""
from enum import Enum

OneK = 1024
OneM = OneK * OneK
OneG = OneM * OneK
OneT = OneG * OneK
OneP = OneT * OneK
OneE = OneP * OneK


class Unit(Enum):
    BYTE = 0
    KB = 1
    MB = 2
    GB = 3
    TB = 4


def convert(num: float, srcUnit: Unit, desUnit: Unit) -> float:
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
            if srcIndex > desIndex:
                num = num * 1024
            else:
                num = num / 1024
            diff -= 1

        return num
    except ValueError:
        return 0


def unitFix(num: float, srcUnit: Unit = Unit.BYTE, maxUnit: Unit = Unit.GB) -> (float, Unit):
    """Automatic conversion to appropriate units"""
    try:
        num = float(num)
        if num == 0:
            return 0, srcUnit

        index = srcUnit.value
        while index < maxUnit.value:
            newNum = num / 1024
            if newNum < 1:
                break
            num = newNum
            index += 1

        return num, Unit(index)
    except ValueError:
        return 0, srcUnit
