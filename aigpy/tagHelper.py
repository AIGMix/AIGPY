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
from mutagen import File
from mutagen import flac
from mutagen import mp4
from mutagen.id3 import TALB, TCOP, TDRC, TIT2, TPE1, TRCK, APIC, TOPE, TCON

def _getHash(pHash, key):
    if key in pHash:
        return pHash[key]
    return ''
    
def _getExtension(filepath):
    index = filepath.rfind('.')
    ret = filepath[index + 1:len(filepath)]
    return str.lower(ret)

def _getFileData(filepath):
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
    if len(array) <= 0:
        return array
    ret = None
    for item in array:
        if ret is None:
            ret = item
            continue
        ret += ';' + item
    return ret

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
        self._handle.tags['copyright'] = self.copyright
        self._handle.tags['tracknumber'] = str(self.tracknumber)
        self._handle.tags['tracktotal'] = str(self.totaltrack)
        self._handle.tags['discnumber'] = str(self.discnumber)
        self._handle.tags['disctotal'] = str(self.totaldisc)
        self._handle.tags['genre'] = self.genre
        self._handle.tags['date'] = self.date
        self._savePic(coverPath)
        self._handle.save()
        return True
    
    def _saveMp4(self, coverPath):
        self._handle.tags['©nam'] = self.title
        self._handle.tags['©alb'] = self.album
        self._handle.tags['aART'] = _getArrayStr(self.albumartist)
        self._handle.tags['©ART'] = _getArrayStr(self.artist)
        self._handle.tags['cprt'] = self.copyright
        self._handle.tags['trkn'] = [[_tryInt(self.tracknumber), _tryInt(self.totaltrack)]]
        self._handle.tags['disk'] = [[_tryInt(self.discnumber), _tryInt(self.totaldisc)]]
        self._handle.tags['©gen'] = self.genre
        self._handle.tags['©day'] = self.date
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
# test.copyright = 'fasd'
# test.title = 'yes'
# test.tracknumber = '1'
# test.genre = 'fdsa'
# test.date = '2019-2-3'
# test.save('e:\\1.jpg')

