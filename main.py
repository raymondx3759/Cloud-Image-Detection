import numpy as np
import cv2
import helper as hlp
from constants import *
import imageFunctions as imf

#List of image filenames such as example below 
paths = ['iss030e187822.nef']

#Convert raw NEF's to BRG arrays and stitch together
imList = imf.convertRawImages(paths, resizeX=resizeX, resizeY=resizeY)
stitched = imf.stitchImages(imList)

#Increase contrast and convert to grayscale
contrast = cv2.convertScaleAbs(stitched, alpha=scaleF, beta=0)
gray = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)

#Blur to remove noise & highpass to isolate
kR, kC = imf.findKSize(gray)
gblur = cv2.GaussianBlur(gray, ksize=(kR, kC), sigmaX=0, sigmaY=0)
highP = cv2.filter2D(gblur, -1, highPassFilter3)
thresh1 = cv2.threshold(highP, 0, maxVal, cv2.THRESH_OTSU)[1]

#Calculate initial mask then open & close and remove mask holes
num = imf.findNum(gray)
mask = hlp.findMask(thresh1, winR=thresh1.shape[1]//25, winC=thresh1.shape[0]//25, num=num)
ellipseK = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (mask.shape[0]//75, mask.shape[1]//75))
opened = cv2.morphologyEx(mask, cv2.MORPH_OPEN, ellipseK)
thresh2 = cv2.threshold(opened, halfVal, maxVal, cv2.THRESH_BINARY)[1]
closed = cv2.morphologyEx(thresh2, cv2.MORPH_CLOSE, ellipseK)
im = hlp.fillMaskHoles(closed)

#List of images which are first converted to RGB for display
imList = [stitched, contrast, gray, gblur, highP, thresh1, mask, opened, closed, im]
imList = imf.convertBRG2RGB(imList)
imf.plotImages(imList,  figX, figY, save=False, show=True)
