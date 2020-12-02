#!/usr/bin/env python
# -*- encoding: utf-8 -*-


'''
@File    :   configHelper.py
@Time    :   2018/12/17
@Author  :   Yaronzz 
@Version :   2.0
@Contact :   yaronhuang@foxmail.com
@Desc    :   Config Tool
'''
import os
import configparser
from binascii import b2a_hex
from binascii import a2b_hex
from Crypto.Cipher import AES

def count(fileName, section=None) -> int:
    """Get para number"""
    try:
        ret = 0
        cf = configparser.ConfigParser()
        cf.read(fileName)
        if section is None:
            seclist = cf.sections()
            for sec in seclist:
                options = cf.options(sec)
                ret = ret + len(options)
        elif cf.has_section(section):
            ret = len(cf[section])
        return ret
    except:
        return 0


def sections(fileName):
    """Get groups"""
    try:
        cf = configparser.ConfigParser()
        cf.read(fileName)
        return cf.sections()
    except:
        return None


def __decrypt__(aesKey, value):
    if aesKey is None or value is None or len(value) <= 0:
        return value
    func = AES_FUNC(aesKey)
    value = func.decrypt(value)
    return value


def __encrypt__(aesKey, value):
    if aesKey is None or value is None or len(value) <= 0:
        return value
    func = AES_FUNC(aesKey)
    real_value = func.encrypt(value)
    real_value = str(real_value, encoding="utf-8")
    return real_value


def getValue(section: str, key: str, default, fileName: str, aesKey=None):
    try:
        cf = configparser.ConfigParser()
        cf.read(fileName)
        if not cf.has_section(section):
            return default
        if key in cf[section]:
            default = cf.get(section, key)
        return __decrypt__(aesKey, default)
    except:
        return __decrypt__(aesKey, default)


def setValue(section, key, value, fileName, aesKey=None):
    try:
        if os.access(fileName, 0) is False:
            fp = open(fileName, "w")
            fp.close()

        cf = configparser.ConfigParser()
        cf.read(fileName)
        if cf.has_section(section) is False:
            cf[section] = {}

        real_value = __encrypt__(aesKey, value)
        cf[section][key] = real_value
        with open(fileName, "w") as f:
            cf.write(f)
        return True
    except:
        return False


def parseNoEqual(fileName):
    ret = {}
    try:
        fd  = open(fileName, 'r')
        arr = fd.readlines()
        group = None
        for item in arr:
            item = item.strip()
            if len(item) <= 0:
                continue
            if item[0] == '#':
                continue
            elif item[0] == '[' and item[len(item) - 1] == ']':
                group = item[1:len(item) - 1]
                ret[group] = []
            elif group is None:
                continue
            else:
                ret[group].append(item)
        return ret     
    except:
        return ret



class AES_FUNC():
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_ECB
        self.AES_LENGTH = 16
        self.cryptor = AES.new(self.pad_key(self.key).encode(), self.mode)

    # 加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
    # 加密内容需要长达16位字符，所以进行空格拼接
    def pad(self, text):
        while len(text) % self.AES_LENGTH != 0:
            text += ' '
        return text

    # 加密密钥需要长达16位字符，所以进行空格拼接
    def pad_key(self, key):
        while len(key) % self.AES_LENGTH != 0:
            key += ' '
        return key

    def encrypt(self, text):
        # 这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
        # 加密的字符需要转换为bytes
        # print(self.pad(text))
        self.ciphertext = self.cryptor.encrypt(self.pad(text).encode())
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext)
        # 解密后，去掉补足的空格用strip() 去掉

    def decrypt(self, text):
        plain_text = self.cryptor.decrypt(a2b_hex(text)).decode()
        return plain_text.rstrip(' ')


