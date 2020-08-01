import numpy as np
import cv2
import scipy.ndimage
import random

#Expands dataset with data augmentation. Produces variety of similar images (flips, contrast, rotations, and zooms) 
def generateImages(im):
    aug = []
    fliph = flipH(im)
    flipv = flipV(im)
    flipb = flipBoth(im)
    bright1 = increaseBright(im, value=30)
    bright2 = increaseBright(im, value=60)
    rot1 = scipy.ndimage.rotate(im, random.randint(-90, 90), cval=255)
    rot2 = scipy.ndimage.rotate(bright1, random.randint(-90, 90), cval=255)
    zoom1 = scipy.ndimage.zoom(im, (random.uniform(1, 2), random.uniform(1, 2), 1))
    zoom2 = scipy.ndimage.zoom(bright1, (random.uniform(1, 2), random.uniform(1, 2), 1))
    aug.extend([fliph, flipv, flipb, bright1, bright2, rot1, rot2, zoom1, zoom2])
    return aug

#Flips image horizontally
def flipH(im):
    return cv2.flip(im, flipCode=0)

#Flips image vertically
def flipV(im):
    return cv2.flip(im, flipCode=1)

#Flips image both horizontally and vertically
def flipBoth(im):
    return cv2.flip(im, flipCode=-1)

#Increases brightness of image by given value 
def increaseBright(im, value):
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    maxV = 255 - value
    v[v > maxV] = 255
    v[v <= maxV] += value
    im = cv2.cvtColor(cv2.merge((h, s, v)), cv2.COLOR_HSV2BGR)
    return im

