import aigpy.netHelper as netHelper

def getInfo(projectName):
    url = 'https://pypi.org/pypi/' + projectName + '/json'
    ret = netHelper.downloadJson(url,None)
    return ret
    
def getLastVersion(projectName):
    ret = getInfo(projectName)
    if ret == None:
        return None
    return ret['info']['version']

def getVersionList(projectName):
    ret = getInfo(projectName)
    if ret == None:
        return None
    return ret['releases']

