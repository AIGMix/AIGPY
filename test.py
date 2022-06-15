#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  server.py
@Date    :  2022/04/13
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :  
"""
import socket
import re

# # AF_INET 表示使用IPv4, SOCK_DGRAM 则表明数据将是数据报(datagrams)
# udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# client_msg = 'Hello world.'

# udp_client.sendto(client_msg.encode('utf8'), ('101.33.238.192', 8081))

# while True:
#     rec_msg, addr = udp_client.recvfrom(1024)
#     print('msg form server:', rec_msg.decode('utf8'))

varDict = {}
varDict['TMP'] = "#001122"

qssStr = "{ color: $TMP%200; }"


def combineColor(color: str, opacity: str):
    if '#' not in color:
        return color
    
    opacity = int(int(opacity) / 100 * 255 + 0.5)
    if opacity < 0:
        opacity = 0
    if opacity > 255:
        opacity = 255
    
    opacity = hex(opacity).replace('0x', '')
    return '#' + opacity + color.replace('#', '')
    

qssStr = re.sub(r'[$](\w+)[%](\w+)([\s;]*)',
                lambda m: '{}{}'.format(combineColor(varDict[m.group(1)], m.group(2)), m.group(3)), qssStr)
# qssStr = re.sub(r'[$](\w+)([\s;]*)', lambda m: '{}{}'.format(varDict[m.group(1)], m.group(2)), qssStr)



pass
