import sys

def myinput(desc):
    v = sys.version_info
    if v[0] > 2:
        return input(desc)
    else:
        return raw_input(desc)
