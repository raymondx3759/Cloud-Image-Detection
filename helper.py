import cv2
import numpy as np
from scipy import signal
from matplotlib import pyplot as plt
from constants import imStrings


#returns array where white pixels are places in im where sums of sparse areas < num
def findMask(im, winR, winC, num):
    #convert image to 1's and 0's
    im = im.astype(bool).astype(int)
    res = np.zeros((im.shape), dtype=np.uint8)
    # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, ksize=(winR, winC))
    kernel = np.ones((winR, winC))
    np.put(kernel, kernel.size // 2, v=0)
    x = signal.convolve2d(im, kernel, mode='same', fillvalue=255)
    res[x < num] = 255
    return res

#calculates gradient magnitude of image
def gradientMag(im):
    imX, imY = np.gradient(im)
    mag = np.sqrt(imX**2 + imY**2)
    return mag

#finds respective corner points which are black pixels that are next to at least 1 white pixel
def findCornerPoints(im):
    #kernel with all values = 1 except middle value which is 0
    kernel = np.ones((3, 3))
    np.put(kernel, kernel.size // 2, v=0)
    
    sums = signal.convolve2d(im, kernel, mode='same')
    sums = sums.astype(bool)
    #finds 4 corner points
    halfR, halfC = sums.shape[0]//2, sums.shape[1]//2
    tl, tr, bl, br = getTL(sums, halfR, halfC), getTR(sums, halfR, halfC), getBL(sums, halfR, halfC), getBR(sums, halfR, halfC)
    tl, tr, bl, br = np.reshape(tl, (1, -1)),  np.reshape(tr, (1, -1)),  np.reshape(bl, (1, -1)),  np.reshape(br, (1, -1)) 
    #arrange found corners into 4x2 array
    corners = np.concatenate((tl, tr, bl, br), axis=0)
    return corners
    
    
#finds most bottom right non zero pixel (which should be corner)
def getBR(sums, halfR, halfC):
    maxRow, maxCol = 0, 0
    for r in range(halfR, sums.shape[0]):
        for c in range(halfC, sums.shape[1]):
            if (sums[r, c] and (r >= maxRow) and (c >= maxCol)):
                    maxRow, maxCol = r, c
    return np.array([maxRow, maxCol])

#finds most top left non zero pixel (which should be corner)
def getTL(sums, halfR, halfC):
    minRow, minCol = sums.shape[0], sums.shape[1]
    for r in range(halfR):
        for c in range(halfC):
             if (sums[r, c] and (r <= minRow) and (c <= minCol)):
                    minRow, minCol = r, c
    return np.array([minRow, minCol])

#finds most top right non zero pixel (which should be corner)
def getTR(sums, halfR, halfC):
    minRow, maxCol = sums.shape[0], 0
    for r in range(halfR):
        for c in range(halfC, sums.shape[1]):
             if (sums[r, c] and (r <= minRow) and (c >= maxCol)):
                    minRow, maxCol = r, c
    return np.array([minRow, maxCol])

#finds most bottom left non zero pixel (which should be corner)
def getBL(sums, halfR, halfC):
    maxRow, minCol = 0, sums.shape[1]
    for r in range(halfR, sums.shape[0]):
        for c in range(halfC):
            if (sums[r, c] and (r >= maxRow) and (c <= minCol)):
                    maxRow, minCol = r, c
    return np.array([maxRow, minCol])

#draws given points (Nx2 matrix) on given image
def drawPoints(im, points):
    for i in range(points.shape[0]):
        im = cv2.circle(im, tuple(points[i][::-1]), 5, color=(255, 255, 255))
    return im

#fills completely surrounded holes in binary image 
def fillMaskHoles(im):
    mask = np.copy(im)
    maxVal = 255

    for i in range(im.shape[1]):
        if (not mask[0, i]):  
            cv2.floodFill(mask, seedPoint=(i, 0), newVal=maxVal, mask=None)
        if (not mask[-1, i]):  
            cv2.floodFill(mask, seedPoint=(i, im.shape[0]-1), newVal=maxVal, mask=None) 

    im[mask == 0] = maxVal
    return im
    

def findKSize(im):
    assert(len(im.shape) == 2)
    kX, kY = im.shape[0] // 100, im.shape[1] // 100
    if (not kX % 2): kX += 1 
    if (not kY % 2): kY += 1
    return (kX, kY) 

def convertBRG2RGB(imList):
    index = 0
    for i in imList:
        imList[index] = cv2.cvtColor(i, code=cv2.COLOR_BGR2RGB)
        index += 1
    return imList

def plotImages(imList, figX, figY):
    plt.figure(figsize=(figX,figY))
    plt.suptitle('Image processing pipeline')
    for i in range(len(imList)):
        plt.subplot(2,5,i+1).set_title(imStrings[i])
        plt.imshow(imList[i])

    plt.show()  