# -*- coding: utf-8 -*-
import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, portrait

def imag2pdf(imaglist, filename):
    try:
        (maxw, maxh) = Image.open(imaglist[0]).size
        c = canvas.Canvas(filename, pagesize=(maxw, maxh))
        for item in imaglist:
            name = os.path.abspath(item)
            c.drawImage(name, 0, 0, maxw, maxh)
            c.showPage()
        c.save()
        return True
    except:
        return False


def path2pdf(path, ext, filename):
    """
    #Func    :   将路径下的图片文件转为pdf(png\jpg)     
    #Param   :   path       图片路径            
    #Param   :   ext        图片扩展名,None则表示无要求           
    #Param   :   filename   输出文件名                
    #Return  :   True/False 
    """
    if os.path.isdir(path) is False:
        return False
    
    array = []
    for root, dirs, files in os.walk(path):
        for item in files:
            if ext == None:
                if '.png' not in item or '.jpg' not in item:
                    continue
            else:
                if ext not in item:
                    continue
            array.append(root + '/' + item)

    return imag2pdf(array, filename)
