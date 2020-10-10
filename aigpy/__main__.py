# -*- coding: utf-8 -*-
from colorama import init
import socks
import requests
import sys
import os
import time

sys.path.append('./')
import aigpy.zipHelper as zipHelper
import aigpy.netHelper as netHelper
from aigpy.updateHelper import updateTool
import aigpy.ffmpegHelper as ffmpegHelper
from aigpy.serverHelper import ServerTool


if __name__ == '__main__':
    os.system("pip install aigpy --upgrade")
    bo =  netHelper.downloadFile('http://down.2zzt.com/uploads/cu/cu2.3.zip', 'e:\\1.zip', showprogress=True)
    init(autoreset=True)
    print("\033[0;30;40m\tHello World\033[0m")  # 黑色
    print("\033[0;31;40m\tHello World\033[0m")  # 红色
    print("\033[0;32;40m\tHello World\033[0m")  # 绿色
    print("\033[0;33;40m\tHello World\033[0m")  # 黄色
    print("\033[0;34;40m\tHello World\033[0m")  # 蓝色
    print("\033[0;35;40m\tHello World\033[0m")  # 紫色
    print("\033[0;36;40m\tHello World\033[0m")  # 浅蓝
    print("\033[0;37;40m\tHello World\033[0m")  # 白色


