import numpy as np
import cv2
""" Constants file """

#Current parameters for implementation. Can be changed to produce different/desired masks
resizeX = 0.2
resizeY = 0.2
figX = 16
figY = 8
scaleF = 2.5
segments = 100
imStrings = ['Composite', 'High Contrast', 'Grayscale', 'Gaussian Blur', 'High Pass', 'Threshold', 'Initial Mask', 'Opened', 'Closed', 'Final Mask']
highPassFilter3 = np.array([[-1, -1, -1], [-1,  8, -1], [-1, -1, -1]])
halfVal = 127
maxVal = 255
maxNum = 10
