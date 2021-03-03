#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   tagHelper.py
@Time    :   2019/07/18
@Author  :   Yaronzz 
@Version :   2.0
@Contact :   yaronhuang@foxmail.com
@Desc    :   
'''
import os
import requests

from mutagen import File
from mutagen import flac
from mutagen import mp4
from mutagen.id3 import TALB, TCOP, TDRC, TIT2, TPE1, TRCK, APIC, TCON, TCOM, TSRC


def __extension__(filepath: str):
    index = filepath.rfind('.')
    ret = filepath[index + 1:len(filepath)]
    return str.lower(ret)


def __content__(filepath: str):
    if filepath is None:
        return None
    if 'http' in filepath:
        re = requests.get(filepath)
        return re.content
    try:
        with open(filepath, "rb") as f:
            data = f.read()
            return data
    except:
        return None


def __tryInt__(obj):
    try:
        ret = int(obj)
        return ret
    except:
        return 0


def __tryStr__(obj):
    return obj if obj is not None else ""


def __tryList__(obj):
    if obj is None or len(obj) <= 0:
        return ''
    return ", ".join(obj)




class TagTool(object):
    def __init__(self, filePath):
        if os.path.isfile(filePath) is False:
            return

        self._filepath = filePath
        self._ext = __extension__(filePath)
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


    def save(self, coverPath: str = None):
        try:
            if 'mp3' in self._ext:
                return self.__saveMp3__(coverPath)
            if 'flac' in self._ext:
                return self.__saveFlac__(coverPath)
            if 'mp4' in self._ext or 'm4a' in self._ext:
                return self.__saveMp4__(coverPath)
            return False
        except Exception as e:
            return False


    def __saveMp3__(self, coverPath):
        if self._handle.tags is None:
            self._handle.add_tags()
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
        self.__savePic__(coverPath)
        self._handle.save()
        return True


    def __saveFlac__(self, coverPath):
        if self._handle.tags is None:
            self._handle.add_tags()
        self._handle.tags['title'] = self.title
        self._handle.tags['album'] = self.album
        self._handle.tags['albumartist'] = self.albumartist
        self._handle.tags['artist'] = self.artist
        self._handle.tags['copyright'] = __tryStr__(self.copyright)
        self._handle.tags['tracknumber'] = str(self.tracknumber)
        self._handle.tags['tracktotal'] = str(self.totaltrack)
        self._handle.tags['discnumber'] = str(self.discnumber)
        self._handle.tags['disctotal'] = str(self.totaldisc)
        self._handle.tags['genre'] = __tryStr__(self.genre)
        self._handle.tags['date'] = __tryStr__(self.date)
        self._handle.tags['composer'] = __tryStr__(self.composer)
        self._handle.tags['isrc'] = str(self.isrc)
        self.__savePic__(coverPath)
        self._handle.save()
        return True

    def __saveMp4__(self, coverPath):
        self._handle.tags['\xa9nam'] = self.title
        self._handle.tags['\xa9alb'] = self.album
        self._handle.tags['aART'] = __tryList__(self.albumartist)
        self._handle.tags['\xa9ART'] = __tryList__(self.artist)
        self._handle.tags['cprt'] = __tryStr__(self.copyright)
        self._handle.tags['trkn'] = [[__tryInt__(self.tracknumber), __tryInt__(self.totaltrack)]]
        self._handle.tags['disk'] = [[__tryInt__(self.discnumber), __tryInt__(self.totaldisc)]]
        self._handle.tags['\xa9gen'] = __tryStr__(self.genre)
        self._handle.tags['\xa9day'] = __tryStr__(self.date)
        self._handle.tags['\xa9wrt'] = __tryList__(self.composer)
        self.__savePic__(coverPath)
        self._handle.save()
        return True


    def __savePic__(self, coverPath):
        data = __content__(coverPath)
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

