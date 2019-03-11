
import os

def getFileSize(path):
    try:
        if os.path.isfile(path) == False:
            return 0
        return os.path.getsize(path)
    except:
        return 0


