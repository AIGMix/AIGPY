#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   dictHelper.py
@Time    :   2020/08/14
@Author  :   Yaronzz
@Version :   1.0
@Contact :   yaronhuang@foxmail.com
@Desc    :   
'''


class DictTool(dict):
    def __init__(self, **kw):
        self.kp = {}
        for k in kw.keys():
            self.__setitem__(k, kw[k])

    def __init__(self, kw):
        self.kp = {}
        for k in kw:
            self.__setitem__(k, kw[k])

    def __contains__(self, k):
        if isinstance(k, str):
            kn = k.lower()
            if not self.kp.__contains__(kn):
                return False
            k = kn
        return super().__contains__(k)

    def __setitem__(self, k, v):
        if isinstance(k, str):
            kn = k.lower()
            self.kp[kn] = k
            k = kn
        super().__setitem__(k, v)

    def __delitem__(self, k):
        if isinstance(k, str):
            k = k.lower()
            self.kp.pop(k)
        super.__delitem__(k)

    def __getitem__(self, k):
        if isinstance(k, str):
            k = k.lower()
        return super().__getitem__(k)

    def actual_key_case(self, k):
        if isinstance(k, str):
            return self.kp[k.lower()]
        return k
