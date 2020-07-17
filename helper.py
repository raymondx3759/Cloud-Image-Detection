import cv2
import numpy as np
from scipy import signal

#returns array where white pixels are places in im where sums of sparse areass < num
def findMask(im, winSize, num):
    #convert image to 1's and 0's
    im = im.astype(bool).astype(int)
    res = np.zeros((im.shape))

    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            if not (i-winSize < 0 or i+winSize >= im.shape[0] or j-winSize < 0 or j+winSize >= im.shape[1]):
                if (np.sum(im[i-winSize:i+winSize, j-winSize:j+winSize]) < num):
                    res[i, j] = 255
    return res

#calculates gradient magnitude of image
def gradientMag(im):
    imX, imY = np.gradient(im)
    mag = np.sqrt(imX**2 + imY**2)
    return mag

#FIND NEAREST BLACK COORD NEXT TO WHITE COORD
def findCornerPoints(im):
    #kernel with all values = 1 except middle value which is 0
    kernel = np.ones((3, 3))
    np.put(kernel, kernel.size // 2, v=0)
    
    sums = signal.convolve2d(im, kernel, mode='same')
    sums = sums.astype(bool)
    
    #finds respective corner points which are black pixels that are next to at least 1 white pixel
    halfR, halfC = sums.shape[0]//2, sums.shape[1]//2
    tl, tr, bl, br = getTL(sums, halfR, halfC), getTR(sums, halfR, halfC), getBL(sums, halfR, halfC), getBR(sums, halfR, halfC)
    tl, tr, bl, br = np.reshape(tl, (1, -1)),  np.reshape(tr, (1, -1)),  np.reshape(bl, (1, -1)),  np.reshape(br, (1, -1)) 
    #arrange found corners into 4x2 array
    corners = np.concatenate((tl, tr, bl, br), axis=0)
    return corners
    
    
    
def getBR(sums, halfR, halfC):
    maxRow, maxCol = 0, 0
    for r in range(halfR, sums.shape[0]):
        for c in range(halfC, sums.shape[1]):
            if (sums[r, c] and (r >= maxRow) and (c >= maxCol)):
                    maxRow, maxCol = r, c
    return np.array([maxRow, maxCol])

def getTL(sums, halfR, halfC):
    minRow, minCol = sums.shape[0], sums.shape[1]
    for r in range(halfR):
        for c in range(halfC):
             if (sums[r, c] and (r <= minRow) and (c <= minCol)):
                    minRow, minCol = r, c
    return np.array([minRow, minCol])

def getTR(sums, halfR, halfC):
    minRow, maxCol = sums.shape[0], 0
    for r in range(halfR):
        for c in range(halfC, sums.shape[1]):
             if (sums[r, c] and (r <= minRow) and (c >= maxCol)):
                    minRow, maxCol = r, c
    return np.array([minRow, maxCol])

def getBL(sums, halfR, halfC):
    maxRow, minCol = 0, sums.shape[1]
    for r in range(halfR, sums.shape[0]):
        for c in range(halfC):
            if (sums[r, c] and (r >= maxRow) and (c <= minCol)):
                    maxRow, minCol = r, c
    return np.array([maxRow, minCol])

#draws given points on image
def drawPoints(im, points):
    for i in range(points.shape[0]):
        im = cv2.circle(im, tuple(points[i][::-1]), 5, color=(255, 255, 255))
    return im

#fills surrounded holes in binary image 
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
    

