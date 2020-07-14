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

stitcher = cv2.Stitcher_create()
im1 = stitcher.stitch((im3, im2, im1))


#FILTERING 
st1 = cv2.convertScaleAbs(im1[1], alpha=2.5, beta=0)
st1 = cv2.cvtColor(st1, cv2.COLOR_BGR2GRAY)
# st1 = cv2.Canny(st1, 100, 200)
sx5 = cv2.getDerivKernels(0, 1, 5, normalize=True)
sx5 = np.outer(sx5[0], sx5[1])
# st1 = cv2.filter2D(st1, -1, sx5)

# hp3 = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])
# hp5 = np.array([ [0,-1,-1,-1,0],[-1,2,-4,2,-1],[-1,-4,13,-4,-1],[-1,2,-4,2,-1],[0,-1,-1,-1,0]   ])
# st1 = cv2.GaussianBlur(st1, ksize=(3,3), sigmaX=1)
# st1 = cv2.filter2D(st1, -1, hp3)
# st1 = cv2.threshold(st1, 40, 255, cv2.THRESH_BINARY)[1]

# se1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7))
# # st1 = cv2.morphologyEx(st1, cv2.MORPH_CLOSE, se1)
# # st1 = cv2.morphologyEx(st1, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3)))
# st2 = np.uint8(find(st1, winSize=20, x=8))
# st2 = cv2.Canny(st2, 127, 255)


st1 = np.uint8(st1)
cv2.imshow('1', im1[1]); 
cv2.imshow('a', st1); 
cv2.waitKey(0)