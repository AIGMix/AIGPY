# -*- coding: utf-8 -*-
import socks
import requests
import sys
import time

sys.path.append('./')
import aigpy.zipHelper as zipHelper
from aigpy.updateHelper import updateTool
import aigpy.ffmpegHelper as ffmpegHelper
from aigpy.serverHelper import ServerTool

def func(httpreq):
    i = 0
    return '111'

if __name__ == '__main__':
    rootDir = 'C:\\Users\\huangyue\\Downloads\\登录界面模板\\后台\\main\\'
    server = ServerTool(rootDir, rootDir)

    server.start('127.0.0.1', 9999)
    while True:
        pass
    plist = []
    plist.append("e:\\test\\1.ini")
    plist.append("e:\\test\\2.ini")
    zipHelper.zip(plist, "e:\\zip.zip")
    zipHelper.unzip("e:\\zip.zip", "e:\\test2")
    print('===VERSION 1.0.0.1===')
    print(sys.argv)

    tf = updateTool(__file__, 'tet', 'http://144.34.241.208//test', '1.0.0.1', 'aigpy.exe', None)
    print(tf.curPath)

    if tf.go() == False:
        print('==OVER!==')
        time.sleep(100)
#    def __run(self, cmd):
#         p = subprocess.Popen(cmd,
#             stdout=subprocess.PIPE, 
#             stderr=subprocess.PIPE,
#             close_fds=True)
#         out, err = p.communicate()
#         out = out.decode('utf8')
#         err = err.decode('utf8')
#         status = p.wait()
#         # check exit status
#         if not os.WIFEXITED(status) or os.WEXITSTATUS(status):
#             if not re.match(r'(iptables|ip6tables): Chain already exists', err):
#                 raise IptablesError(cmd, err)
#         return out
