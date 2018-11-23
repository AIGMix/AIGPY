import os

def mkdirs(path):
    path = path.strip()
    path = path.rstrip("\\")
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    else:
        return False

def replaceLimiChar(path, newChar):
    if path is None:
        return ""
    path.replace(':', newChar)
    path.replace('/', newChar)
    path.replace('?', newChar)
    path.replace('<', newChar)
    path.replace('>', newChar)
    path.replace('|', newChar)
    path.replace('\\', newChar)
    path.replace('*', newChar)
    path.replace('\"', newChar)
    return path
