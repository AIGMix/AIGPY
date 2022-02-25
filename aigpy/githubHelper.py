#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  githubHelper.py
@Date    :  2022/02/07
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :  
"""

import requests

class GistFile(object):
    def __init__(self, name, url, content) -> None:
        self.name = name
        self.url = url
        self.content = content

def getGistFiles(gistId):
    array = []
    try:
        respond = requests.get(f'https://api.github.com/gists/{gistId}')
        if respond.status_code == 200:
            files = respond.json()['files']
            for key in files:
                item = files[key]
                array.append(GistFile(item['filename'], item['raw_url'], item['content']))
        return array
    except:
        return array
