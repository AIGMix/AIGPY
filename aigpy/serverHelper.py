#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
@File    :   serverHelper.py
@Time    :   2019/04/10
@Author  :   Yaronzz 
@Version :   2.0
@Contact :   yaronhuang@foxmail.com
@Desc    :   
'''

# -*- coding=utf-8 -*-
import socket

from aigpy.threadHelper import ThreadTool
from aigpy.threadHelper import ThreadPoolManger
from aigpy.httpHelper   import HttpRequest

class ServerTool(object):
    def __init__(self, rootDir,cookieDir,fileOf404=None,scfamily=socket.AF_INET,sctype=socket.SOCK_STREAM):
        """
        #Func    :   初始化     
        #Param   :   rootDir    [in] 根目录     
        #Param   :   cookieDir  [in] cookie目录     
        #Param   :   fileOf404  [in] 404文件        
        #Param   :   scfamily   [in] 网络family     
        #Param   :   sctype     [in] 网络类型       
        """
        rootDir.replace('\\', '/')
        cookieDir.replace('\\', '/')
        self.__sockHandle    = None
        self.__sockFamily    = scfamily
        self.__sockType      = sctype
        self.__rootDir       = rootDir + '/'
        self.__cookieDir     = cookieDir + '/'
        self.__fileOf404     = fileOf404
        self.__requestFunc   = None
        self.__listenThread  = ThreadTool(1)
        self.__requestThread = ThreadPoolManger(5)
        self.__revieveLen    = 1024

    def __requestThreadCall__(self, sock, addr):
        body     = None
        request  = sock.recv(self.__revieveLen)
        http_req = HttpRequest(self.__rootDir, self.__cookieDir, self.__fileOf404)
        http_req.passRequest(request)

        if self.__requestFunc is not None:
            body = self.__requestFunc(http_req)
        sock.send(http_req.getResponse(body).encode('utf-8'))
        sock.close()

    def __listenThreadCall__(self):
        while True:
            sock, addr = self.__sockHandle.accept()
            self.__requestThread.addWork(self.__requestThreadCall__, *(sock, addr))
        self.start()
    def start(self, address, port, requestFuc=None, listenNum=10, recieveLen=1024):
        """
        #Func    :   启动
        #Param   :   address    [in] ip地址 
        #Param   :   port       [in] 端口号
        #Param   :   requestFuc [in] 响应函数,参数为httpRequest,返回body     
        #Param   :   listenNum  [in] 监听的数量
        #Param   :   recieveLen [in] 数据包的长度
        #Return  :   True/False   
        """
        try:
            self.stop()
            self.__revieveLen  = recieveLen
            self.__requestFunc = requestFuc
            self.__sockHandle  = socket.socket(self.__sockFamily, self.__sockType)
            self.__sockHandle.bind((address, int(port)))
            self.__sockHandle.listen(listenNum)
            self.__listenThread.start(self.__listenThreadCall__)
            return True
        except:
            return False

    def stop(self):
        if self.__sockHandle is None:
            return
        self.__listenThread.close()
        self.__requestThread.close()
        self.__sockHandle.close()




