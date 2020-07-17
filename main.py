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

#create stitch class and stich images together
stitcher = cv2.Stitcher_create()
im1 = stitcher.stitch((im3, im2, im1))

#FILTERING 
st1 = cv2.convertScaleAbs(im1[1], alpha=2.5, beta=0)
st1 = cv2.cvtColor(st1, cv2.COLOR_BGR2GRAY)
gray = np.copy(st1)

"""  Homography testing / need to refine
# mag = gradientMag(st1)
# corners = findCornerPoints(mag)
# dstCoords = np.array([[0, 0], [0, st1.shape[1]], [st1.shape[0], 0], [st1.shape[0], st1.shape[1]]])
# # st2 = drawPoints(st1, corners)
# # dstCoords = np.array([ [0, 0], [0, 500], [500, 0], [500, 500]])
# H, mask = cv2.findHomography(corners, dstCoords,method=cv2.RANSAC, ransacReprojThreshold=5)
# st2 = cv2.warpPerspective(st1, H, dsize=(st1.shape[1], st1.shape[0]))
"""


hp3 = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]]) #works beetter
h3 = np.array([[-1, -1, -1], [-1,  8, -1], [-1, -1, -1]])

st1 = cv2.GaussianBlur(st1, ksize=(3,3), sigmaX=1)
st1 = cv2.filter2D(st1, -1, hp3)
st1 = cv2.threshold(st1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

se1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
st1 = cv2.morphologyEx(st1, cv2.MORPH_CLOSE, se1)
st1 = cv2.erode(st1, kernel=se1)
st1 = np.uint8(findMask(st1, winSize=25, num=4))

contours, hierarchy = cv2.findContours(st1, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
st1 = cv2.drawContours(st1, contours, -1, (255,255,255), thickness=cv2.FILLED)
thresh = cv2.threshold(st1, 127, 255, cv2.THRESH_BINARY)[1]

thresh = fillMaskHoles(thresh)
#close to get rid of jagged edges
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11,11)))

            

st1 = np.uint8(st1)
cv2.imshow('1', st1); 
cv2.imshow('a', thresh); 
cv2.waitKey(0)



