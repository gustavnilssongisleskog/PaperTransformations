import numpy as np
import cv2 as cv
from numpy import ndarray
import open3d

from src.space.matrices import calibrate

paper_width = 21
paper_height = 29.7
paper_corners_3d = np.array([
    [0, 0, 0],
    [paper_width, 0, 0],
    [paper_width, paper_height, 0],
    [0, paper_height, 0]
], dtype=np.float32)

def paper_3d_and_color(img: ndarray, paper_corners_2d: ndarray, paper_img_width: int) -> tuple:
    rmse, cam_mtx, dist, rvec, tvec = calibrate(paper_corners_3d, paper_corners_2d)

    paper_img_height = int(paper_img_width * paper_height / paper_width)
    paper_points_3d = np.array([[[x, y, 0] for x in np.linspace(0, paper_width, paper_img_width)] for y in np.linspace(0, paper_height, paper_img_height)])
    paper_points_3d = paper_points_3d.reshape(-1, 3)


    projected, _ = cv.projectPoints(paper_points_3d, rvec, tvec, cam_mtx, dist)
    projected = projected.reshape(-1, 2)

    colors = np.array([img[int(y), int(x), :] for (x, y) in projected], dtype=np.uint8)

    return paper_points_3d, colors

def paper_straight_on(img: ndarray, paper_corners_2d: ndarray, paper_img_width: int) -> ndarray:
    _, colors = paper_3d_and_color(img, paper_corners_2d, paper_img_width)

    paper_img_height = int(paper_img_width * paper_height / paper_width)
    colors = colors.reshape((paper_img_height, paper_img_width, 3))
    return colors

def paper_pointcloud(img: ndarray, paper_corners_2d: ndarray, paper_img_width: int):
    paper_points_3d, colors = paper_3d_and_color(img, paper_corners_2d, paper_img_width)

    pointcloud = open3d.geometry.PointCloud()
    pointcloud.points = open3d.utility.Vector3dVector(paper_points_3d)
    pointcloud.colors = open3d.utility.Vector3dVector(colors / 255)
    open3d.visualization.draw_geometries([pointcloud])

