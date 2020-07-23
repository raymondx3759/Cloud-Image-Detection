import numpy as np
import cv2
import helper as hlp
from constants import *
import imageFunctions as imf

#NEXT STEPS: PLAY ATOUND W CONTRAST TO SEE WHICH VAL GIVES BEST FOR LST1
# THEN FIND WAY TO RELATE BRIGHTNESS TO CONTRAST FOR ALL 3 IMAGES

# lst = ["iss035e017200.nef"]
lst = ['iss035e020930.nef']
# lst = ['iss030e187822.nef']
# lst = ['iss030e163191.nef', 'iss030e163192.nef', 'iss030e163193.nef']
imList = imf.convertRawImages(lst, resizeX=0.2, resizeY=0.2)
stitched = imf.stitchImages(imList)

#Filtering
contrast = cv2.convertScaleAbs(stitched, alpha=2.5, beta=0)
gray = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)

h3 = np.array([[-1, -1, -1], [-1,  8, -1], [-1, -1, -1]])
kx, ky = imf.findKSize(gray)
gblur = cv2.GaussianBlur(gray, ksize=(kx, ky), sigmaX=0, sigmaY=0)
highP = cv2.filter2D(gblur, -1, h3)
thresh1 = cv2.threshold(highP, 0, 255, cv2.THRESH_OTSU)[1]
# thresh1 = cv2.threshold(highP, 50, 255, cv2.THRESH_BINARY)[1]

mask = hlp.findMask(thresh1, winR=thresh1.shape[1]//25, winC=thresh1.shape[0]//25, num=10)
opened = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (mask.shape[0]//75, mask.shape[1]//75)))
thresh2 = cv2.threshold(opened, 127, 255, cv2.THRESH_BINARY)[1]
closed = cv2.morphologyEx(thresh2, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (thresh2.shape[0]//75, thresh2.shape[1]//75)))
im = hlp.fillMaskHoles(closed)

#Plotting images
imList = [stitched, contrast, gray, gblur, highP, thresh1, mask, opened, closed, im]
imList = imf.convertBRG2RGB(imList)

# imf.plotImages(imList, figX, figY)
cv2.imshow('', mask); cv2.imshow('a', stitched); cv2.waitKey(0)

