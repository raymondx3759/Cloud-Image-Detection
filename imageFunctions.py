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
    brightness = np.mean(im)
    closest = scale[np.abs(scale - brightness).argmin()]
    print (int(brightness), closest)
    kR, kC = im.shape[0]/segments, im.shape[1]/segments
    print (kR, kC)
    kR += getSigmoid(brightness)
    kC += getSigmoid(brightness)
    kR, kC = roundPosOdd(kR), roundPosOdd(kC)
    return kR, kC

        
def getSigmoid(x):
    L, k, h, y = 20, 0.03, 90, -5
    val = (L / (1 + np.exp(-k * (x - h)))) + y
    print ("val=", val)
    return val

#Finds nearest odd integer > 1 given float. Rounds up with ties
def roundPosOdd(n):
    if (n < 3): return 3
    if (not (n % 2)): return int(n - 1)
    return int(2*np.floor(n/2) + 1)
 
    

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