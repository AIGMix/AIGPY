import socks
import requests
import sys
import time

sys.path.append('./')
import aigpy.zipHelper as zipHelper
from aigpy.updateHelper import updateTool
import aigpy.ffmpegHelper as ffmpegHelper

if __name__ == '__main__':
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
