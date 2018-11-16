import os
import configparser

def GetValue(section, key, fileName):
    cf = configparser.ConfigParser()
    cf.read(fileName)
    if cf.has_section(section) == False:
        return

    for item in cf[section]:
        if item == key:
            str = cf.get(section, key)
            return str


def SetValue(section, key, value, fileName):
    if os.access(fileName, 0) == False:
        fp = open(fileName, "w")
        fp.close()

    cf = configparser.ConfigParser()
    cf.read(fileName)
    if cf.has_section(section) == False:
        cf[section] = {}

    cf[section][key] = value
    with open(fileName, "w") as f:
        cf.write(f)
