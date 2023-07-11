import cv2 as cv
import numpy as np
from numpy import ndarray
from typing import Tuple


img_height = 4608
img_width = 3456
cx, cy = img_width / 2, img_height / 2

intrinsic_guess = np.array([
    [1, 0, cx],
    [0, 1, cy],
    [0, 0, 1]
])

paper_width = 21
paper_height = 29.7
paper_corners_3d = np.array([
    [0, 0, 0],
    [paper_width, 0, 0],
    [paper_width, paper_height, 0],
    [0, paper_height, 0],
    [paper_width / 2, paper_height / 2, 0]
], dtype=np.float32)

def calibrate_corners(paper_corners_2d: ndarray) -> tuple:
    # calibrate using both the corners and the middle of the paper
    def line(a, b) -> tuple:
        return (b[1] - a[1]), (a[0] - b[0]), (a[1] * b[0] - a[0] * b[1])
    
    a1, b1, c1 = line(paper_corners_2d[0], paper_corners_2d[2])
    a2, b2, c2 = line(paper_corners_2d[1], paper_corners_2d[3])
    
    center = -1 / (a1 * b2 - a2 * b1) * np.array([[b2, -b1], [-a2, a1]]) @ np.array([c1, c2])
    points_img = np.concatenate((paper_corners_2d, center.reshape(1, 2)))
    
    return calibrate(paper_corners_3d, points_img)
    

def calibrate(points_3d: ndarray, points_img: ndarray) -> tuple:
    rmse, cam_mtx, dist, rvecs, tvecs = cv.calibrateCamera([np.array(points_3d, dtype=np.float32)], [np.array(points_img, dtype=np.float32)], (img_width, img_height), intrinsic_guess, np.zeros(5))

    rvec = rvecs[0]
    tvec = tvecs[0]

    return rmse, cam_mtx, dist, rvec, tvec


def extrinsics_to_mtx(rvec: ndarray, tvec: ndarray) -> ndarray:
    R, _ = cv.Rodrigues(rvec)
    mtx = np.zeros(4, 4)
    mtx[:3, :3] = R

    mtx[:3, 3] = tvec
    mtx[3, 3] = 1

    return mtx