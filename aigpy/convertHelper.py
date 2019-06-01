# -*- coding: utf-8 -*-

def convertStorageUnit(num, srcUnit, desUnit):
    """
    #Func    :   存储单位转换               
    #Param   :   num        [in]   数字              
    #Param   :   srcUnit    [in]   来源单位(gb/mb/kb/byte)          
    #Param   :   desUnit    [in]   目标单位(gb/mb/kb/byte)                    
    #Return  :   None:Err 
    """
    try:
        units = ['gb','mb','kb','byte']
        if srcUnit not in units or desUnit not in units:
            return None
        if srcUnit == desUnit:
            return num
        num = float(num)
        if num == 0:
            return 0
        srcIndex = units.index(srcUnit)
        desIndex = units.index(desUnit)
        tmp = desIndex - srcIndex
        while tmp != 0:
            if srcIndex < desIndex:
                num = num * 1024
            else:
                num = num / 1024
            if tmp > 0:
                tmp = tmp - 1
            else:
                tmp = tmp + 1
        return num
    except:
        return None

def convertStorageUnitToString(num, srcUnit):
    """
    #Func    :   将存储单位转为字符串           
    #Param   :   num       [in] 值     
    #Param   :   srcUnit   [in] 单位     
    """
    try:
        units = ['gb', 'mb', 'kb', 'byte']
        if srcUnit not in units:
            return '0 KB'
        num = float(num)
        srcIndex = units.index(srcUnit)
        if srcIndex == 0:
            return str(round(num, 2)) + ' ' + units[0].upper()
        
        tmp = num
        while srcIndex != 0:
            num = num / 1024
            if num < 1:
                return str(round(tmp, 2)) + ' ' + units[srcIndex].upper()
            tmp = num
            srcIndex = srcIndex - 1
        return str(round(tmp, 2)) + ' ' + units[srcIndex].upper()
    except:
        return '0 KB'
