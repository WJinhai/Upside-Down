import os
import pickle

import cv2
import numpy as np
from tqdm import tqdm
from utils import isRotationMatrix, rotationMatrixToEulerAngles


def match(tupian, xiaoyang):
    MIN_MATCH_COUNT = 10

    tupian = os.path.join('data/kkf', tupian)
    xiaoyang = os.path.join('data/kkf', xiaoyang)

    img1 = cv2.imread(xiaoyang, 0)
    img2 = cv2.imread(tupian, 0)

    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1, des2, k=2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)

    # print(len(good))
    if len(good) > MIN_MATCH_COUNT:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

        np.savez('pts.npz', src_pts=src_pts, dst_pts=dst_pts)

        H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        return H

    else:
        print("Not enough matches are found - %d/%d" % (len(good), MIN_MATCH_COUNT))
        return None


def get_roll(H):
    data = np.load('calib.npz')
    K = data['mtx']

    num, Rs, Ts, Ns = cv2.decomposeHomographyMat(H, K)

    # print(num)
    for i in range(num):
        R = Rs[i]
        if isRotationMatrix(R):
            angles = rotationMatrixToEulerAngles(R)
            # print(angles)
            return abs(angles[2])
    return 0


if __name__ == '__main__':
    with open('data.pkl', 'rb') as f:
        samples = pickle.load(f)

    num_tests = 0
    num_correct = 0

    for sample in tqdm(samples):
        # print(sample)
        idx = sample['idx']
        tupian = sample['image']
        xiaoyang = sample['xiaoyang']
        result = sample['result']
        is_real = sample['real']

        if result == 1:
            H = match(tupian, xiaoyang)
            roll = get_roll(H)
            if roll > 1.57 or roll < -1.57:
                to_real = 1
            else:
                to_real = 0
            if is_real == to_real:
                num_correct += 1
            num_tests += 1

    print('num_tests: ' + str(num_tests))
    print('num_correct: ' + str(num_correct))
    print('acc: ' + str(num_correct / num_tests))
