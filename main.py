from PIL import Image
import numpy as np
import cv2
import rawpy
from helper import *


#Read raw1 image from NEF format
raw1, raw2, raw3 = rawpy.imread('Images/iss030e163193.nef'), rawpy.imread('Images/iss030e163192.nef'), rawpy.imread('Images/iss030e163191.nef')
im1, im2, im3 = Image.fromarray(raw1.postprocess()), Image.fromarray(raw2.postprocess()), Image.fromarray(raw3.postprocess())
#Convert to np array and to BGR
im1, im2, im3 = cv2.cvtColor(np.asarray(im1), cv2.COLOR_RGB2BGR), cv2.cvtColor(np.asarray(im2), cv2.COLOR_RGB2BGR), cv2.cvtColor(np.asarray(im3), cv2.COLOR_RGB2BGR)
im1, im2, im3 = cv2.resize(im1, dsize=(0,0), fx=.2, fy=0.2), cv2.resize(im2, dsize=(0,0), fx=.2, fy=0.2), cv2.resize(im3, dsize=(0,0), fx=.2, fy=0.2)


# r2 = rawpy.imread('iss032e012419.nef')
# r2 = cv2.cvtColor(np.asarray(im1), cv2.COLOR_RGB2BGR)
# r2 = cv2.resize(r2, dsize=(0,0), fx=.2, fy=0.2)

#Stitch images together
stitcher = cv2.Stitcher_create()
_, stitched = stitcher.stitch((im3, im2, im1))

#FILTERING 
im = cv2.convertScaleAbs(stitched, alpha=2.5, beta=0)
im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
gray = np.copy(im)

"""  Homography testing / need to refine
# mag = gradientMag(im)
# corners = findCornerPoints(mag)
# dstCoords = np.array([[0, 0], [0, im.shape[1]], [im.shape[0], 0], [im.shape[0], im.shape[1]]])
# # st2 = drawPoints(im, corners)
# # dstCoords = np.array([ [0, 0], [0, 500], [500, 0], [500, 500]])
# H, mask = cv2.findHomography(corners, dstCoords,method=cv2.RANSAC, ransacReprojThreshold=5)
# st2 = cv2.warpPerspective(im, H, dsize=(im.shape[1], im.shape[0]))
"""

hp3 = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]]) #works better
h3 = np.array([[-1, -1, -1], [-1,  8, -1], [-1, -1, -1]])

im = cv2.GaussianBlur(im, ksize=(3,3), sigmaX=1)
im = cv2.filter2D(im, -1, hp3)
im = cv2.threshold(im, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

structElem = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
im = cv2.erode(im, kernel=structElem) 
im = findMask(im, winX=im.shape[1]//25, winY=im.shape[0]//25, num=5)


im = cv2.morphologyEx(im, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (im.shape[0]//30, im.shape[1]//30)))
im = cv2.threshold(im, 127, 255, cv2.THRESH_BINARY)[1]
im = fillMaskHoles(im)
# im = cv2.erode(im, kernel=structElem) #be conservative maybe


            

im = np.uint8(im)
cv2.imshow('1', im); 
cv2.imshow('gray', gray); 
cv2.waitKey(0)



