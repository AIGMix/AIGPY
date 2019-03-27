#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   zipHelper.py
@Time    :   2019/03/01
@Author  :   Yaron Huang 
@Version :   1.0
@Contact :   yaronhuang@qq.com
@Desc    :   Zip Tool
'''

import os
import zipfile
import tarfile

"""
#Func    :   Get zip type
#Param   :   para-zip object
#Return  :   0:filepath 1:dir 2:filepathlist
"""
def _getParaType(para):
    try:
        if os.path.isfile(para):
            return 0
    except:
        pass
    try:
        if os.path.isdir(para):
            return 1
    except:
        pass
    return 2

def _getZipType(zipName):
    try:
        name = os.path.basename(zipName)
        if name.lower().find('.tar') > 0:
            return 'tar'
        else:
            return 'zip'
    except:
        pass

def _open(zipName, ptype, mode='w'):
    try:
        if ptype == 'tar':
            pZip = tarfile.open(zipName, mode)
        else:
            pZip = zipfile.ZipFile(zipName, mode, zipfile.ZIP_DEFLATED)
        return pZip
    except:
        return None

def _write(pZip, ptype, pfilename, parcname):
    try:
        if ptype == 'tar':
            pZip.add(pfilename, arcname=parcname)
        else:
            pZip.write(pfilename, arcname=parcname)
        return True
    except:
        return False


def zip(para, zipName):
    """
    #Func    :   zip files or dir       
    #Param   :   para      file | file[] | dir      
    #Param   :   zipName   outPathName      
    #Return  :   True/False         
    """
    check = _getParaType(para)
    ptype = _getZipType(zipName)
    try: 
        pZip = _open(zipName, ptype)
        if check == 2:
            for file in para:
                pZip._write(pZip, ptype, file, os.path.basename(file))
        if check == 0:
            pZip._write(pZip, ptype, para, os.path.basename(para))
        if check == 1:
            name = os.path.dirname(para)
            for dirpath, dirnames, filenames in os.walk(para):
                fpath = dirpath.replace(name, '')
                fpath = fpath and fpath + os.sep or ''
                for filename in filenames:
                    pZip._write(pZip, ptype, os.path.join(dirpath, filename), fpath +filename)
        pZip.close()
        return True
    except:
        return False

def unzip(zipName, outPath):
    """
    #Func    :   解压缩     
    #Param   :   zipName [in]  压缩包名字       
    #Param   :   outPath [in]  输出目录            
    #Return  :   True/False 
    """
    ptype = _getZipType(zipName)
    try:
        pZip = _open(zipName, ptype, 'r')
        pZip.extractall(path=outPath)
        pZip.close()
        return True
    except:
        return False

