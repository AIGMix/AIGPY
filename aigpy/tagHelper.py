#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   tagHelper.py
@Time    :   2019/07/18
@Author  :   Yaron Huang 
@Version :   1.0
@Contact :   yaronhuang@qq.com
@Desc    :   
'''
import os
import sys
import requests
from mutagen import File
from mutagen import flac
from mutagen import mp4
from mutagen.id3 import TALB, TCOP, TDRC, TIT2, TPE1, TRCK, APIC, TCON, TCOM, TSRC
from aigpy import pathHelper
import aigpy.netHelper as netHelper


def _getHash(pHash, key):
    if key in pHash:
        return pHash[key]
    return ''


def _lower(inputs):
    if isinstance(inputs, str):
        inputs = inputs.decode('utf-8')
    inputs = inputs.lower().encode('utf-8')
    return inputs


def _getExtension(filepath):
    index = filepath.rfind('.')
    ret = filepath[index + 1:len(filepath)]
    v = sys.version_info
    if v[0] > 2:
        return str.lower(ret)
    else:
        return _lower(ret)


def _getFileData(filepath):
    if 'http' in filepath:
        re = requests.get(filepath)
        return re.content
    try:
        with open(filepath, "rb") as f:
            data = f.read()
            return data
    except:
        return None


def _tryInt(obj):
    try:
        ret = int(obj)
        return ret
    except:
        return 0


def _getArrayStr(array):
    if array is None:
        return ''
    if len(array) <= 0:
        return array
    ret = None
    for item in array:
        if ret is None:
            ret = item
            continue
        ret += ', ' + item
    return ret


def _noneToEmptyString(obj):
    if obj is None:
        return ''
    else:
        return obj


class TagTool(object):
    def __init__(self, filePath):
        if os.path.isfile(filePath) is False:
            return

        self._filepath = filePath
        self._ext = _getExtension(filePath)
        self._handle = File(filePath)

        self.title = ''
        self.album = ''
        self.albumartist = ''
        self.artist = ''
        self.copyright = ''
        self.tracknumber = ''
        self.totaltrack = ''
        self.discnumber = ''
        self.totaldisc = ''
        self.genre = ''
        self.date = ''
        self.composer = ''
        self.isrc = ''

    def save(self, coverPath=None):
        try:
            if 'mp3' in self._ext:
                return self._saveMp3(coverPath)
            if 'flac' in self._ext:
                return self._saveFlac(coverPath)
            if 'mp4' in self._ext or 'm4a' in self._ext:
                return self._saveMp4(coverPath)
            return False
        except:
            return False

    def _saveMp3(self, coverPath):
        self._handle.tags.add(TIT2(encoding=3, text=self.title))
        self._handle.tags.add(TALB(encoding=3, text=self.album))
        # self._handle.tags.add(TOPE(encoding=3, text=self.albumartist))
        self._handle.tags.add(TPE1(encoding=3, text=self.artist))
        self._handle.tags.add(TCOP(encoding=3, text=self.copyright))
        self._handle.tags.add(TRCK(encoding=3, text=str(self.tracknumber)))
        # self._handle.tags.add(TRCK(encoding=3, text=self.discnum))
        self._handle.tags.add(TCON(encoding=3, text=self.genre))
        self._handle.tags.add(TDRC(encoding=3, text=self.date))
        self._handle.tags.add(TCOM(encoding=3, text=self.composer))
        self._handle.tags.add(TSRC(encoding=3, text=self.isrc))
        self._savePic(coverPath)
        self._handle.save()
        return True

    def _saveFlac(self, coverPath):
        if self._handle.tags is None:
            self._handle.add_tags()
        self._handle.tags['title'] = self.title
        self._handle.tags['album'] = self.album
        self._handle.tags['albumartist'] = self.albumartist
        self._handle.tags['artist'] = self.artist
        self._handle.tags['copyright'] = _noneToEmptyString(self.copyright)
        self._handle.tags['tracknumber'] = str(self.tracknumber)
        self._handle.tags['tracktotal'] = str(self.totaltrack)
        self._handle.tags['discnumber'] = str(self.discnumber)
        self._handle.tags['disctotal'] = str(self.totaldisc)
        self._handle.tags['genre'] = _noneToEmptyString(self.genre)
        self._handle.tags['date'] = _noneToEmptyString(self.date)
        self._handle.tags['composer'] = _noneToEmptyString(self.composer)
        self._handle.tags['isrc'] = str(self.isrc)
        self._savePic(coverPath)
        self._handle.save()
        return True

    def _saveMp4(self, coverPath):
        self._handle.tags['\xa9nam'] = self.title
        self._handle.tags['\xa9alb'] = self.album
        self._handle.tags['aART'] = _getArrayStr(self.albumartist)
        self._handle.tags['\xa9ART'] = _getArrayStr(self.artist)
        self._handle.tags['cprt'] = _noneToEmptyString(self.copyright)
        self._handle.tags['trkn'] = [[_tryInt(self.tracknumber), _tryInt(self.totaltrack)]]
        self._handle.tags['disk'] = [[_tryInt(self.discnumber), _tryInt(self.totaldisc)]]
        self._handle.tags['\xa9gen'] = _noneToEmptyString(self.genre)
        self._handle.tags['\xa9day'] = _noneToEmptyString(self.date)
        self._handle.tags['\xa9wrt'] = _getArrayStr(self.composer)
        self._savePic(coverPath)
        self._handle.save()
        return True

    def _savePic(self, coverPath):
        data = _getFileData(coverPath)
        if data is None:
            return
        if 'flac' in self._ext:
            pic = flac.Picture()
            pic.data = data
            if '.jpg' in coverPath:
                pic.mime = u"image/jpeg"
            self._handle.clear_pictures()
            self._handle.add_picture(pic)
        if 'mp3' in self._ext:
            self._handle.tags.add(APIC(encoding=3, data=data))
        if 'mp4' in self._ext or 'm4a' in self._ext:
            pic = mp4.MP4Cover(data)
            self._handle.tags['covr'] = [pic]

# test = TagTool('e:\\1.m4a')
# test.album = ['ff']
# test.albumartist = ['yaron', 'f']
# test.artist = ['huang', 'dd']
# test.copyright = None
# test.title = 'yes'
# test.tracknumber = '1'
# test.genre = 'fdsa'
# test.date = '2019-2-3'
# test.save('e:\\1.jpg')
# y =str.lower("Ye")

# t = str("Ye").lower()
# a = o
