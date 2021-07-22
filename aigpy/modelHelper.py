#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   jsonHelper.py
@Time    :   2020/08/10
@Author  :   Yaronzz
@Version :   2.0
@Contact :   yaronhuang@foxmail.com
@Desc    :  
"""
from aigpy.dictHelper import DictTool


class ModelBase(object):
    pass


def modelToDict(model):
    if model is None:
        return None
    if not __isModel__(model):
        return None

    pr = {}
    for name in dir(model):
        value = getattr(model, name)
        if name[0] == '_':
            continue
        if callable(value):
            continue
        if __isModelList__(value):
            value = modelListToDictList(value)
        if __isModel__(value):
            value = modelToDict(value)
        pr[name] = value
    return pr


def dictToModel(indict, model):
    if indict is None or model is None:
        return None
    ret = model.__class__()
    maps = DictTool(indict)

    for key in dir(ret):

        if key[0] == '_':
            continue
        if key.lower() not in maps:
            if __isObject__(getattr(ret, key)):
                setattr(ret, key, None)
            continue

        # 判断是否为字典数组
        lvalue = maps[key.lower()]
        if __isDictList__(lvalue):
            value = dictListToModelList(lvalue, getattr(ret, key))
        # 判断是否为字典
        elif __isDict__(lvalue):
            value = dictToModel(lvalue, getattr(ret, key))
        else:
            value = lvalue

        setattr(ret, key, value)
    return ret


def dictListToModelList(jList, model):
    if jList is None or model is None:
        return jList
    ret = []
    for item in jList:
        data = dictToModel(item, model)
        ret.append(data)
    return ret


def modelListToDictList(mList):
    if mList is None:
        return mList
    ret = []
    for item in mList:
        data = modelToDict(item)
        ret.append(data)
    return ret


def __isDict__(data):
    if isinstance(data, dict):
        return True
    return False


def __isObject__(data):
    if isinstance(data, object):
        return True
    return False


def __isDictList__(data):
    if isinstance(data, list):
        for item in data:
            return __isDict__(item)
    return False


def __isModelList__(data):
    if isinstance(data, list):
        return True
    return False


def __isModel__(data):
    return isinstance(data, ModelBase)
