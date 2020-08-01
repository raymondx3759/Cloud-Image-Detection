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
    brightness = np.mean(im)
    kR, kC = im.shape[0]/segments, im.shape[1]/segments
    sig = getSigmoid(brightness)
    kR, kC = roundPosOdd(kR+sig), roundPosOdd(kC+sig)
    return kR, kC

        
#Sigmoid function with parameters as listed below. Given an x value, calculates output from curve
#Parameters chosen such that function endpoints are (0, -5) and (200, 15)
def getSigmoid(x):
    L, k, h, y = 20, 0.045, 80, -5
    val = (L / (1 + np.exp(-k * (x - h)))) + y
    return val

#Finds nearest odd integer >= 3 given float. Rounds down with ties
def roundPosOdd(n):
    if (n < 3): return 3
    if (not (n % 2)): return int(n - 1)
    return int(2*np.floor(n/2) + 1)
    
#Finds number from 0 to maxNum based on given image brightness using exponential fitting with the modifiable parameters A, b, k
#The parameter A controls the width of the curve with higher values of A resulting in smaller widths
#The parameter b controls the steepness of the curve with higher values of b resulting in steeper dropoffs
#The parameter k controls the y-intercept of the curve. With the current parameters, k is set so that it is maxNum + 1
def findNum(im, A=-1, b=0.012, k=maxNum+1):
    assert(len(im.shape) == 2)
    brightness = np.mean(im)
    num = int(np.rint((A * np.exp(b * brightness)) + k))
    return num    

#Since openCV stores images as BGR, images may need to be converted to be shown correctly
#Converts given list of images from BGR to RGB 
def convertBRG2RGB(imList):
    index = 0
    for i in imList:
        imList[index] = cv2.cvtColor(i, code=cv2.COLOR_BGR2RGB)
        index += 1
    return imList

#Shows steps of image pipeline in pyplot with figure of provided size
def plotImages(imList, figX, figY, save=True, show=True):
    plt.figure(figsize=(figX,figY))
    plt.suptitle('Image Processing Pipeline')
    for i in range(len(imList)):
        plt.subplot(2,5,i+1).set_title(imStrings[i])
        plt.imshow(imList[i])

    if (save): plt.savefig('pipeline.pdf')
    if (show): plt.show()  