#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import tarfile
import zipfile


def __getParaType__(para):
    '''
    @return
        0: file path
        1: dir path
        2: file paths
    '''
    if os.path.isfile(para):
        return 0
    if os.path.isdir(para):
        return 1
    return 2

def __getZipType__(zipName):
    '''
    @return
        tar
        zip
    '''
    name = os.path.basename(zipName)
    if name.lower().find('.tar') > 0:
        return 'tar'
    else:
        return 'zip'

def __open__(zipName, zipType, mode = 'w'):
    if zipType == 'tar':
        return tarfile.open(zipName, mode)
    else:
        return zipfile.ZipFile(zipName, mode, zipfile.ZIP_DEFLATED)

def __write__(pZip, zipType, filename, parcname):
    if zipType == 'tar':
        pZip.add(filename, arcname=parcname)
    else:
        pZip.write(filename, arcname=parcname)


def zip(inPath, outPath):
    '''zip files or path

    @param
        inPath: file path/file paths/dir
        output: zip file pathname
    @return
        True/False
    '''
    try:
        paraType = __getParaType__(inPath)
        zipType = __getZipType__(outPath)
        pZip = __open__(outPath, zipType)

        if paraType == 2:
            for file in inPath:
                pZip.__write__(pZip, zipType, file, os.path.basename(file))

        if paraType == 0:
            pZip.__write__(pZip, zipType, inPath, os.path.basename(inPath))

        if paraType == 1:
            name = os.path.dirname(inPath)
            for dirpath, dirnames, filenames in os.walk(inPath):
                path = dirpath.replace(name, '')
                path = path and path + os.sep or ''
                for filename in filenames:
                    pZip.__write__(pZip, zipType, os.path.join(dirpath, filename), path + filename)

        pZip.close()
        return True
    except:
        return False


def unzip(zipName, outPath):
    zipType = __getZipType__(zipName)
    try:
        pZip = __open__(zipName, zipType, 'r')
        pZip.extractall(path = outPath)
        pZip.close()
        return True
    except:
        return False
