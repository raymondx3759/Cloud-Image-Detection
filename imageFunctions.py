from PIL import Image
import numpy as np
import cv2
import rawpy
from matplotlib import pyplot as plt
import helper as hlp
from constants import *

#Reads every image from given list of paths and converts & resizes them to np arrays
def convertRawImages(paths, resizeX=1, resizeY=1):
    imList = []
    for image in paths:
        image = "Images/" + image
        curr = Image.fromarray(rawpy.imread(image).postprocess())
        curr = cv2.cvtColor(np.asarray(curr), cv2.COLOR_RGB2BGR)
        curr = cv2.resize(curr, None, fx=resizeX, fy=resizeY)
        imList.append(curr)
    return imList

#Stitchs images from imList together into one composite image
def stitchImages(imList):
    if (len(imList) == 1):
        return imList[0]
    stitcher = cv2.Stitcher_create(mode=cv2.STITCHER_SCANS)
    retVal, stitched = stitcher.stitch(tuple(imList))
    if (retVal != 0):
        print ('Error stitching images together')
        exit(1)
    return stitched

