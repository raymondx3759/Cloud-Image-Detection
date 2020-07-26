import numpy as np
import cv2
import helper as hlp
from constants import *
import imageFunctions as imf

#Download more images

# paths = ['iss035e020930.nef'] #189 39 GUCCI
# paths = ['iss030e187822.nef'] #266 54 GUCCI
# paths = ['iss030e163191.nef', 'iss030e163192.nef', 'iss030e163193.nef'] #323 60
# paths = ["iss035e017200.nef"] #300 62 kinda bad
paths = ['iss032e012755.nef']

imList = imf.convertRawImages(paths, resizeX=resizeX, resizeY=resizeY)
stitched = imf.stitchImages(imList)

#Filtering
contrast = cv2.convertScaleAbs(stitched, alpha=scaleF, beta=betaF)
gray = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)

kR, kC = imf.findKSize(gray)
gblur = cv2.GaussianBlur(gray, ksize=(kR, kC), sigmaX=0, sigmaY=0)
highP = cv2.filter2D(gblur, -1, highPassFilter3)
thresh1 = cv2.threshold(highP, 0, maxVal, cv2.THRESH_OTSU)[1]

mask = hlp.findMask(thresh1, winR=thresh1.shape[1]//25, winC=thresh1.shape[0]//25, num=num)
opened = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (mask.shape[0]//75, mask.shape[1]//75)))
thresh2 = cv2.threshold(opened, halfVal, maxVal, cv2.THRESH_BINARY)[1]
closed = cv2.morphologyEx(thresh2, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (thresh2.shape[0]//75, thresh2.shape[1]//75)))
im = hlp.fillMaskHoles(closed)

#Plotting images
imList = [stitched, contrast, gray, gblur, highP, thresh1, mask, opened, closed, im]
imList = imf.convertBRG2RGB(imList)

# imf.plotImages(imList, figX, figY)
cv2.imshow('', stitched); cv2.imshow('a', im); cv2.waitKey(0)

