import os

def mkdirs(path):
    path = path.strip()
    path = path.rstrip("\\")
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    return False

def replaceLimitChar(path, newChar):
    if path is None:
        return ""
    if newChar is None:
        newChar = ''
    path = path.replace(':', newChar)
    path = path.replace('：', newChar)
    path = path.replace('/', newChar)
    path = path.replace('?', newChar)
    path = path.replace('<', newChar)
    path = path.replace('>', newChar)
    path = path.replace('|', newChar)
    path = path.replace('\\', newChar)
    path = path.replace('*', newChar)
    path = path.replace('\"', newChar)
    return path

def getDirName(filepath):
    filepath = filepath.replace('\\', '/')
    index    = filepath.rfind('/')
    if index == -1:
        return './'
    return filepath[0:index+1]

def getFileName(filepath):
    filepath = filepath.replace('\\', '/')
    index = filepath.rfind('/')
    if index == -1:
        return filepath
    return filepath[index+1:len(filepath)]

def getFileNameWithoutExtension(filepath):
    filepath = getFileName(filepath)
    index = filepath.rfind('.')
    if index == -1:
        return filepath
    return filepath[0:index]

def getFileExtension(filepath):
    filepath = getFileName(filepath)
    index = filepath.rfind('.')
    if index == -1:
        return
    return filepath[index:len(filepath)]


