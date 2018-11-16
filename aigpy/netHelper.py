import sys
import requests
import json

def downloadString(url, timeout=(3.05, 27)):
    try:
        re = requests.get(url, timeout)
        return re.content
    except:
        return
    
def downloadJson(url, timeout=(3.05, 27)):
    try:
        re = requests.get(url, timeout)
        info = json.loads(re.content)
        return info
    except:
        return

def downloadFile(url, fileName):
    if sys.version_info > (2, 7):
        from urllib.request import urlopen
    else:
        from urllib2 import urlopen

    try:
        response = urlopen(url)
        chunk = 16 * 1024
        with open(fileName, 'wb') as f:
            while True:
                chunk = response.read(chunk)
                if not chunk:
                    break
                f.write(chunk)
            return True
    except:
        return False
