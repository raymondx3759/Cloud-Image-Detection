import cv2
import numpy as np

#30
def find(im, winSize, x):
    res = np.zeros((im.shape[0], im.shape[1]))
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            if not (i-winSize < 0 or i+winSize >= im.shape[0] or j-winSize < 0 or j+winSize >= im.shape[1]):
                win = im[i-winSize:i+winSize, j-winSize:j+winSize]
                if (np.sum(win) < (255*x)):
                    res[i, j] = 255
    return res


