from PIL import Image
import numpy as np
import cv2
import rawpy
from matplotlib import pyplot as plt
import helper as hlp
from constants import *

#Read raw1 image from NEF format
raw1, raw2, raw3 = rawpy.imread('Images/iss030e163193.nef'), rawpy.imread('Images/iss030e163192.nef'), rawpy.imread('Images/iss030e163191.nef')
im1, im2, im3 = Image.fromarray(raw1.postprocess()), Image.fromarray(raw2.postprocess()), Image.fromarray(raw3.postprocess())
#Convert to np array and to BGR
im1, im2, im3 = cv2.cvtColor(np.asarray(im1), cv2.COLOR_RGB2BGR), cv2.cvtColor(np.asarray(im2), cv2.COLOR_RGB2BGR), cv2.cvtColor(np.asarray(im3), cv2.COLOR_RGB2BGR)
im1, im2, im3 = cv2.resize(im1, None, fx=resizeX, fy=resizeY), cv2.resize(im2, None, fx=resizeX, fy=resizeY), cv2.resize(im3, None, fx=resizeX, fy=resizeY)

#Stitch images together
stitcher = cv2.Stitcher_create(mode=cv2.STITCHER_SCANS)
_, stitched = stitcher.stitch((im3, im2, im1))

#FILTERING 
contrast = cv2.convertScaleAbs(stitched, alpha=2.5, beta=0)
gray = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)


h3 = np.array([[-1, -1, -1], [-1,  8, -1], [-1, -1, -1]]) #works better
kx, ky = hlp.findKSize(gray)
gblur = cv2.GaussianBlur(gray, ksize=(kx, ky), sigmaX=0, sigmaY=0)
highP = cv2.filter2D(gblur, -1, h3)
thresh1 = cv2.threshold(highP, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


mask = hlp.findMask(thresh1, winR=thresh1.shape[1]//25, winC=thresh1.shape[0]//25, num=10)
opened = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (mask.shape[0]//75, mask.shape[1]//75)))
thresh2 = cv2.threshold(opened, 127, 255, cv2.THRESH_BINARY)[1]
closed = cv2.morphologyEx(thresh2, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (thresh2.shape[0]//75, thresh2.shape[1]//75)))
im = hlp.fillMaskHoles(closed)
# im = cv2.erode(im, kernel=structElem) #be conservative

#Plotting images\
#NEED TO CONVERT IMAGES
imList = [stitched, contrast, gray, gblur, highP, thresh1, mask, opened, closed, im]
imList = hlp.convertBRG2RGB(imList)

hlp.plotImages(imList, figX, figY)


