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

def calibrate(points_3d: ndarray, points_img: ndarray) -> tuple:
    rmse, cam_mtx, dist, rvecs, tvecs = cv.calibrateCamera([points_3d], [points_img], (img_width, img_height), intrinsic_guess, np.zeros(5))

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