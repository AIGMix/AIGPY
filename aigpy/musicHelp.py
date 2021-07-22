#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  musicHelp.py
@Date    :  2021/05/13
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :  
"""
from aigpy.modelHelper import ModelBase


class MusicBase(ModelBase):
    id = ''
    name = ''


class User(MusicBase):
    pass


class Artist(MusicBase):
    pass


class Track(MusicBase):
    pass


class Album(MusicBase):
    artists = Artist()
    tracks = Track()


class Show(MusicBase):
    pass


class Playlist(MusicBase):
    isOwn = False
    tracks = Track()

# class AccountData(object):
#     def __init__(self, dbPath: str):
#         self.db = sqlite3.connect(dbPath)

#     def __creatFollowTable__(self):
