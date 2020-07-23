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




lst = convertRawImages(['Images/iss030e187822.nef'], resizeX=0.2, resizeY=0.2)
stitched = stitchImages(lst)
# cv2.imshow('', stitched); cv2.waitKey(0)

# print (np.sum(stitched) / stitched.size)
contrast = cv2.convertScaleAbs(stitched, alpha=2.5, beta=0)
gray = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)
# print (np.sum(gray) / gray.size)



h3 = np.array([[-1, -1, -1], [-1,  8, -1], [-1, -1, -1]]) #works better

kx, ky = hlp.findKSize(gray)
gblur = cv2.GaussianBlur(gray, ksize=(kx, ky), sigmaX=0, sigmaY=0)
highP = cv2.filter2D(gblur, -1, h3)
thresh1 = cv2.threshold(highP, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

mask = hlp.findMask(thresh1, winR=thresh1.shape[1]//25, winC=thresh1.shape[0]//25, num=10)
# opened = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (mask.shape[0]//75, mask.shape[1]//75)))
# thresh2 = cv2.threshold(opened, 127, 255, cv2.THRESH_BINARY)[1]
# closed = cv2.morphologyEx(thresh2, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (thresh2.shape[0]//75, thresh2.shape[1]//75)))
# im = hlp.fillMaskHoles(closed)
# im = cv2.erode(im, kernel=structElem) #be conservative

#Plotting images
cv2.imshow('gray', thresh1)
cv2.imshow('thesh', mask)
cv2.waitKey(0)


