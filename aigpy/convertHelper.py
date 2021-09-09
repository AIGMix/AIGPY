#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  convertHelper.py
@Date    :  2020/11/16
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :  
"""
from aigpy.memoryHelper import Unit, unitFix


def getMemoryUnitString(num: float, unit: Unit) -> str:
    """Convert the unit to string, eg: num(2653)unit(MB) -> '2.59 GB'

    Args:
        num (float): value
        unit (MemoryUnit): Original unit

    Returns:
        [string]: target string, keep two decimal places
    """
    value, newUnit = unitFix(num, unit)
    string = str(round(value, 2)) + ' ' + newUnit.name
    return string
