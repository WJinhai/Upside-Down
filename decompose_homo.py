import cv2
import numpy as np

from utils import isRotationMatrix, rotationMatrixToEulerAngles

data = np.load('calib.npz')
K = data['mtx']
print(K)

data = np.load('homo.npz')
H = data['homo']
print(H)

num, Rs, Ts, Ns = cv2.decomposeHomographyMat(H, K)

print(num)
for i in range(num):
    R = Rs[i]
    if isRotationMatrix(R):
        angles = rotationMatrixToEulerAngles(R)
        print(angles)
# print(Ts)
# print(Ns)
