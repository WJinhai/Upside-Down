import time

import cv2
import numpy as np
from tqdm import tqdm

data = np.load('pts.npz')
src_pts = data['src_pts']
dst_pts = data['dst_pts']

num_tests = 100000
start = time.time()
for _ in tqdm(range(num_tests)):
    H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)


elapsed_time = time.time() - start
print('average time per image pair: {} seconds'.format(elapsed_time / num_tests))
