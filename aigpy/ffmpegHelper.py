import subprocess
import os

def mergerByM3u8(url, filepath, showshell=False):
    try:
        cmd = "ffmpeg -safe 0 -i " + url + " -c copy -bsf:a aac_adtstoasc \"" + filepath + "\""
        if showshell:
            res = subprocess.call(cmd, shell=True)
        else:
            res = subprocess.call(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res != 0:
            return False
        return True
    except:
        return False

def mergerByFiles(srcfilepaths, filepath, showshell=False):
    result = True
    tmpfile = filepath + "TMP.txt"
    try:
        with open(tmpfile, 'w') as fd:
            for item in srcfilepaths:
                fd.write('file \'' + item + '\'\n')

        cmd = "ffmpeg -f concat -safe 0 -i \"" + tmpfile + "\" -c copy \"" + filepath + "\""
        if showshell:
            res = subprocess.call(cmd, shell=True)
        else:
            res = subprocess.call(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res != 0:
            result = False
    except:
        result = False

    if os.access(tmpfile,0):
        os.remove(tmpfile)
    return result
