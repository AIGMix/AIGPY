#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   httpHelper.py
@Time    :   2019/04/10
@Author  :   Yaron Huang 
@Version :   1.0
@Contact :   yaronhuang@qq.com
@Desc    :   
'''

import os
import xml.dom.minidom

CONTENT_404 = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <style type="text/css">
        div{
            width: 100%;
            text-align:center;
        }
    </style>
</head>
<body>
    <div>
        <h1>404 Not Found</h1>
    </div>
</body>
<html>
'''


# 返回码
class ErrorCode(object):
    OK        = "HTTP/1.1 200 OK\r\n"
    NOT_FOUND = "HTTP/1.1 404 Not Found\r\n"

# 将字典转成字符串
def dict2str(d):
    s = ''
    for i in d:
        s = s + i+': '+d[i]+'\r\n'
    return s

class Session(object):
    def __init__(self):
        self.data = dict()
        self.cook_file = None

    def getCookie(self, key):
        if key in self.data.keys():
            return self.data[key]
        return None

    def setCookie(self, key, value):
        self.data[key] = value

    def loadFromXML(self):
        import xml.dom.minidom as minidom
        root = minidom.parse(self.cook_file).documentElement
        for node in root.childNodes:
            if node.nodeName == '#text':
                continue
            else:
                self.setCookie(node.nodeName, node.childNodes[0].nodeValue)

    def write2XML(self):
        import xml.dom.minidom as minidom
        dom = xml.dom.minidom.getDOMImplementation().createDocument(None, 'Root', None)
        root = dom.documentElement
        for key in self.data:
            node = dom.createElement(key)
            node.appendChild(dom.createTextNode(self.data[key]))
            root.appendChild(node)
        print(self.cook_file)
        with open(self.cook_file, 'w') as f:
            dom.writexml(f, addindent='\t', newl='\n', encoding='utf-8')


class HttpRequest(object):
    def __init__(self, rootDir, cookieDir, fileOf404=None):
        self.RootDir       = rootDir
        self.CookieDir     = cookieDir
        self.NotFoundHtml  = fileOf404
        self.method        = None
        self.url           = None
        self.protocol      = None
        self.head          = dict()
        self.Cookie        = None
        self.session       = None
        self.request_data  = dict()
        self.response_line = ''      # 错误码
        self.response_head = dict()  # 返回数据类型
        self.response_body = ''      # 返回的数据

    def __readNotFoundHtml__(self):
        try:
            if self.NotFoundHtml is not None:
                fd  = open(self.NotFoundHtml, 'r')
                ret = fd.read()
                fd.close()
                return ret
        except:
            pass
        return CONTENT_404

    def __passRequestLine__(self, request_line):
        header_list = request_line.split(' ')
        self.method = header_list[0].upper()
        self.url    = header_list[1]
        if self.url == '/':
            self.url = '/index.html'
        self.protocol = header_list[2]

    def __passRequestHead__(self, request_head):
        head_options = request_head.split('\r\n')
        for option in head_options:
            key, val = option.split(': ', 1)
            self.head[key] = val
        if 'Cookie' in self.head:
            self.Cookie = self.head['Cookie']

    def passRequest(self, request):
        request = request.decode('utf-8')
        if len(request.split('\r\n', 1)) != 2:
            return
        request_line, body = request.split('\r\n', 1)
        request_head       = body.split('\r\n\r\n', 1)[0]     
        self.__passRequestLine__(request_line)
        self.__passRequestHead__(request_head)
        # 所有post视为动态请求
        if self.method == 'POST':
            self.request_data = {}
            request_body = body.split('\r\n\r\n', 1)[1]
            parameters = request_body.split('&')   # 每一行是一个字段
            for i in parameters:
                if i == '':
                    continue
                key, val = i.split('=', 1)
                self.request_data[key] = val
            self.dynamicRequest(self.RootDir + self.url)
        # get如果带参数视为动态请求,不带参数的get视为静态请求
        if self.method == 'GET':
            if self.url.find('?') != -1:        
                self.request_data = {}
                req   = self.url.split('?', 1)[1]
                s_url = self.url.split('?', 1)[0]
                parameters = req.split('&')
                for i in parameters:
                    key, val = i.split('=', 1)
                    self.request_data[key] = val
                self.dynamicRequest(self.RootDir + s_url)
            else:
                self.staticRequest(self.RootDir + self.url)

    # 只提供制定类型的静态文件
    def staticRequest(self, path):
        bIsNotFound =  True
        if os.path.isfile(path):
            bIsNotFound    = False
            extension_name = os.path.splitext(path)[1]
            extension_set  = {'.css', '.html', '.js'}
            if extension_name == '.py':
                self.dynamicRequest(path)
            else:    
                fd  = open(path, 'rb')
                txt = fd.read()
                fd.close()
                self.response_line = ErrorCode.OK
                self.response_body = txt
                if extension_name == '.png':
                    self.response_head['Content-Type'] = 'text/png'
                elif extension_name in extension_set:
                    self.response_head['Content-Type'] = 'text/html'
                else:
                    bIsNotFound = True
        if bIsNotFound:
            self.response_line = ErrorCode.NOT_FOUND
            self.response_head['Content-Type'] = 'text/html'
            self.response_body = self.__readNotFoundHtml__()
            
    def __processSession__(self):
        self.session = Session()
        # 没有提交cookie，创建cookie
        if self.Cookie is None:
            self.Cookie = self.__generateCookie__()
            cookie_file = self.CookieDir + self.Cookie
            self.session.cook_file = cookie_file
            self.session.write2XML()
        else:
            cookie_file = self.CookieDir + self.Cookie
            self.session.cook_file = cookie_file
            if os.path.exists(cookie_file):
                self.session.loadFromXML()
            # 当前cookie不存在，自动创建
            else:
                self.Cookie = self.__generateCookie__()
                cookie_file = self.CookieDir+self.Cookie
                self.session.cook_file = cookie_file
                self.session.write2XML()
        return self.session

    def __generateCookie__(self):
        import time
        import hashlib
        cookie = str(int(round(time.time() * 1000)))
        hl = hashlib.md5()
        hl.update(cookie.encode(encoding='utf-8'))
        return cookie

    def dynamicRequest(self, path):
        # 如果找不到或者后缀名不是py则输出404
        if not os.path.isfile(path) or os.path.splitext(path)[1] != '.py':
            self.response_line = ErrorCode.NOT_FOUND
            self.response_head['Content-Type'] = 'text/html'
            self.response_body = self.__readNotFoundHtml__()
        else:
            # 获取文件名，并且将/替换成.
            file_path = path.split('.', 1)[0].replace('/', '.')
            self.response_line = ErrorCode.OK
            m = __import__(file_path)
            m.main.SESSION = self.__processSession__()
            if self.method == 'POST':
                m.main.POST = self.request_data
                m.main.GET = None
            else:
                m.main.POST = None
                m.main.GET = self.request_data
            self.response_body = m.main.app()
            self.response_head['Content-Type'] = 'text/html'
            self.response_head['Set-Cookie']   = self.Cookie

    def getResponse(self, body=None):
        if body is None:
            return self.response_line+dict2str(self.response_head)+'\r\n'+self.response_body
        else:
            return self.response_line+dict2str(self.response_head)+'\r\n'+body
