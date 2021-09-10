#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   tagHelper.py
@Time    :   2019/07/18
@Author  :   Yaronzz 
@Version :   2.0
@Contact :   yaronhuang@foxmail.com
@Desc    :  
"""
import os

import requests
from mutagen import File
from mutagen import flac
from mutagen import mp4
from mutagen.id3 import TALB, TCOP, TDRC, TIT2, TPE1, TRCK, APIC, TCON, TCOM, TSRC, USLT


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
        self.lyrics = ''

        self.__load__()

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
            return False, str(e)

    def addPic(self, converPath: str = None):
        try:
            self.__savePic__(converPath)
            self._handle.save()
            return True
        except Exception as e:
            return False, str(e)

    def addLyrics(self, lyrics: str = None):
        try:
            if 'mp3' in self._ext:
                self._handle.tags.add(USLT(encoding=3, lang=u'eng', desc=u'desc', text=__tryStr__(self.lyrics)))
            if 'flac' in self._ext:
                self._handle.tags['lyrics'] = __tryStr__(self.lyrics)
            if 'mp4' in self._ext or 'm4a' in self._ext:
                self._handle.tags['\xa9lyr'] = __tryStr__(self.lyrics)
            self._handle.save()
            return True
        except Exception as e:
            return False, str(e)

    def __load__(self):
        try:
            if 'mp3' in self._ext:
                return self.__getMp3__()
            if 'flac' in self._ext:
                return self.__getFlac__()
            if 'mp4' in self._ext or 'm4a' in self._ext:
                return self.__getMp4__()
        except:
            return

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
        self._handle.tags.add(USLT(encoding=3, lang=u'eng', desc=u'desc', text=self.lyrics))
        self.__savePic__(coverPath)
        self._handle.save()
        return True

    def __getMp3__(self):
        if self._handle.tags is None:
            self._handle.add_tags()

    def __saveFlac__(self, coverPath):
        if self._handle.tags is None:
            self._handle.add_tags()
        self._handle.tags['title'] = self.title
        self._handle.tags['album'] = self.album
        self._handle.tags['albumartist'] = __tryList__(self.albumartist)
        self._handle.tags['artist'] = __tryList__(self.artist)
        self._handle.tags['copyright'] = __tryStr__(self.copyright)
        self._handle.tags['tracknumber'] = str(self.tracknumber)
        self._handle.tags['tracktotal'] = str(self.totaltrack)
        self._handle.tags['discnumber'] = str(self.discnumber)
        self._handle.tags['disctotal'] = str(self.totaldisc)
        self._handle.tags['genre'] = __tryStr__(self.genre)
        self._handle.tags['date'] = __tryStr__(self.date)
        self._handle.tags['composer'] = __tryStr__(self.composer)
        self._handle.tags['isrc'] = __tryStr__(self.isrc)
        self._handle.tags['lyrics'] = __tryStr__(self.lyrics)
        self.__savePic__(coverPath)
        self._handle.save()
        return True

    def __getFlac__(self):
        if self._handle.tags is None:
            return
        self.title = self.__getTagItem__('title')
        self.album = self.__getTagItem__('album')
        self.albumartist = self.__getTagItem__('albumartist')
        self.artist = self.__getTagItem__('artist')
        self.copyright = self.__getTagItem__('copyright')
        self.tracknumber = self.__getTagItem__('tracknumber')
        self.totaltrack = self.__getTagItem__('tracktotal')
        self.discnumber = self.__getTagItem__('discnumber')
        self.totaldisc = self.__getTagItem__('disctotal')
        self.genre = self.__getTagItem__('genre')
        self.date = self.__getTagItem__('date')
        self.composer = self.__getTagItem__('composer')
        self.isrc = self.__getTagItem__('isrc')
        self.lyrics = self.__getTagItem__('lyrics')

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
        self._handle.tags['\xa9lyr'] = __tryStr__(self.lyrics)
        self.__savePic__(coverPath)
        self._handle.save()
        return True

    def __getMp4__(self):
        self.title = self.__getTagItem__('\xa9nam')
        self.album = self.__getTagItem__('\xa9alb')
        self.albumartist = self.__getTagItem__('aART')
        self.artist = self.__getTagItem__('\xa9ART')
        self.copyright = self.__getTagItem__('\cprt')
        self.tracknumber = self.__getTagItem__('trkn')
        self.totaltrack = self.__getTagItem__('trkn')
        self.discnumber = self.__getTagItem__('disk')
        self.totaldisc = self.__getTagItem__('disk')
        self.genre = self.__getTagItem__('\xa9gen')
        self.date = self.__getTagItem__('\xa9day')
        self.composer = self.__getTagItem__('\xa9wrt')
        self.lyrics = self.__getTagItem__('\xa9lyr')

    def __getTagItem__(self, name):
        if name in self._handle.tags:
            return self._handle.tags[name]
        return ''

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
