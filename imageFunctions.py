from PIL import Image
import numpy as np
import cv2
import rawpy
from matplotlib import pyplot as plt
from constants import *

#Reads NEF images from given list of paths and converts & resizes to np arrays
#Returns list of resized and grayscale images
def convertRawImages(paths, resizeX=1, resizeY=1):
    imList = []
    for image in paths:
        image = "Images/" + image
        curr = Image.fromarray(rawpy.imread(image).postprocess())
        curr = cv2.cvtColor(np.asarray(curr), cv2.COLOR_RGB2BGR)
        curr = cv2.resize(curr, None, fx=resizeX, fy=resizeY)
        imList.append(curr)
    return imList

#Stitchs images from imList together and returns the composite image
def stitchImages(imList):
    if (len(imList) == 1):
        return imList[0]
    stitcher = cv2.Stitcher_create(mode=cv2.STITCHER_SCANS)
    retVal, stitched = stitcher.stitch(tuple(imList))
    if (retVal != 0):
        print ('Error stitching images together')
        exit(1)
    return stitched

#Finds odd and positive kernel size based on image width and height
def findKSize(im):
    assert(len(im.shape) == 2)
    kX, kY = im.shape[0] // 100, im.shape[1] // 100
    if (not kX % 2): kX += 1 
    if (not kY % 2): kY += 1
    return (kX, kY) 

#Since openCV stores images as BGR, images may need to be converted to be shown correctly
#Converts given list of images from BGR to RGB 
def convertBRG2RGB(imList):
    index = 0
    for i in imList:
        imList[index] = cv2.cvtColor(i, code=cv2.COLOR_BGR2RGB)
        index += 1
    return imList

#Shows steps of image pipeline in pyplot with figure of provided size
def plotImages(imList, figX, figY):
    plt.figure(figsize=(figX,figY))
    plt.suptitle('Image processing pipeline')
    for i in range(len(imList)):
        plt.subplot(2,5,i+1).set_title(imStrings[i])
        plt.imshow(imList[i])

    plt.show()  