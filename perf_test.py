import time

import cv2
import numpy as np
from tqdm import tqdm

from utils import isRotationMatrix, rotationMatrixToEulerAngles

data = np.load('calib.npz')
K = data['mtx']
print(K)

data = np.load('homo.npz')
H = data['homo']
print(H)

num_tests = 100000
start = time.time()
for _ in tqdm(range(num_tests)):

    num, Rs, Ts, Ns = cv2.decomposeHomographyMat(H, K)

    # print(num)
    for i in range(num):
        R = Rs[i]
        if isRotationMatrix(R):
            angles = rotationMatrixToEulerAngles(R)
            # print(angles)

elapsed_time = time.time() - start
print('average time per image pair: {} seconds'.format(elapsed_time / num_tests))
