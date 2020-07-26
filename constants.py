import numpy as np

""" Constants file """

#Current parameters for implementation. Can be changed to produce different/desired masks
resizeX = 0.2
resizeY = 0.2
figX = 20
figY = 8
scaleF = 2.5
betaF = 0
segments = 100
imStrings = ['stitched', 'contrast', 'gray', 'gblur', 'highP', 'thresh1', 'mask', 'opened', 'closed', 'im']
highPassFilter3 = np.array([[-1, -1, -1], [-1,  8, -1], [-1, -1, -1]])
halfVal = 127
maxVal = 255
num = 10

