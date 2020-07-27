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
    #only 1 image passed; just return it 
    if (len(imList) == 1):
        return imList[0]
    stitcher = cv2.Stitcher_create(mode=cv2.STITCHER_SCANS)
    retVal, stitched = stitcher.stitch(tuple(imList))
    if (retVal != 0):
        print ('Error stitching images together')
        exit(1)
    return stitched

#Finds odd & positive kernel size for filtering based on image brightness and dimensions
def findKSize(im):
    assert(len(im.shape) == 2)
    #play around w range values??
    lower, upper, step = 30, 80, 5
    scale = np.asarray([i for i in range(lower, upper, step)])
    mean = np.mean(im)
    closest = scale[np.abs(scale - mean).argmin()]
    print (int(mean), closest)
    kR, kC = findK(im)
    print ("findK", kR, kC)
    if closest < 40: return kR - 2, kC - 2
    elif closest < 50:
        # return (5, 5)
        return kR, kC
    elif closest < 55: return kR, kC
    elif closest < 60: return kR, kC
    elif closest < 65: return kR+2, kC+2
    elif closest < 70: return kR, kC
    else: return kR + 4, kC + 4

#Finds nearest odd integer given float. Rounds up with ties
def roundOdd(n):
    return int(2*np.floor(n/2) + 1)
 
 #finds kernel size based on image dimensions
def findK(im):
    assert(len(im.shape) == 2)
    kR, kC = im.shape[0]/segments, im.shape[1]/segments
    kR, kC = roundOdd(kR), roundOdd(kC)
    return (kR, kC)
    

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