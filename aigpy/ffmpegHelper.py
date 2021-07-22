#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# coding:utf-8
"""
@File    :   ffmpegHelper.py
@Time    :   2018/12/17
@Author  :   Yaron Huang 
@Version :   1.0
@Contact :   yaronhuang@qq.com
@Desc    :  
"""
import asyncio
import subprocess
import sys


def convert(srcPath, descPath, bitrate: int = 1600):
    command = (
        'ffmpeg -v quiet -y -i "%s" -acodec libmp3lame -abr true '
        f"-b:a {bitrate} "
        '-af "apad=pad_dur=2, dynaudnorm, loudnorm=I=-17" "%s"'
    )

    if sys.platform == "win32":
        formattedCommand = command % (
            str(srcPath),
            str(descPath),
        )
    else:
        formattedCommand = command % (
            str(srcPath).replace("$", r"\$"),
            str(descPath).replace("$", r"\$"),
        )

    process = subprocess.Popen(
        formattedCommand,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    _, proc_err = process.communicate()

    if process.returncode != 0:
        message = "Convert failed." + proc_err.decode('utf-8')
        return False, message

    return True, ""


def isEnable():
    try:
        process = subprocess.Popen(
            ['ffmpeg', '-version'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8"
        )
    except FileNotFoundError:
        return False

    return True

# t = isEnable()
# convert('e://test.webm', 'e://test.mp3', 159489)
