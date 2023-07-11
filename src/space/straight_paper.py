import numpy as np
import cv2 as cv
from numpy import ndarray
from src.space.matrices import paper_height, paper_width

def paper_3d_and_color(img: ndarray, paper_img_width: int, cam_mtx: ndarray, dist: ndarray, rvec: ndarray, tvec: ndarray) -> tuple:

    paper_img_height = int(paper_img_width * paper_height / paper_width)
    paper_points_3d = np.array([[[x, y, 0] for x in np.linspace(0, paper_width, paper_img_width)] for y in np.linspace(0, paper_height, paper_img_height)])
    paper_points_3d = paper_points_3d.reshape(-1, 3)


    projected, _ = cv.projectPoints(paper_points_3d, rvec, tvec, cam_mtx, dist)
    projected = projected.reshape(-1, 2)

    colors = np.array([img[int(y), int(x), :] for (x, y) in projected], dtype=np.uint8)

    return paper_points_3d, colors

def paper_straight_on(img: ndarray, paper_img_width: int, cam_mtx: ndarray, dist: ndarray, rvec: ndarray, tvec: ndarray) -> ndarray:
    _, colors = paper_3d_and_color(img, paper_img_width, cam_mtx, dist, rvec, tvec)

    paper_img_height = int(paper_img_width * paper_height / paper_width)
    colors = colors.reshape((paper_img_height, paper_img_width, 3))
    return colors