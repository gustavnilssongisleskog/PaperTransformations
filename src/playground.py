import cv2 as cv
import numpy as np
from numpy import ndarray
from typing import Tuple
from matrices import *
from matplotlib import pyplot as plt
from straight_paper import paper_straight_on, paper_pointcloud

num_photos = 4

paths = [f"C:/Users/ggisl/Desktop/PaperTransformations/images/IMG_0{i}.jpg" for i in range(num_photos)]
corners0 = [
    [680, 870],
    [2017, 730],
    [3211, 2176],
    [1613, 2695]
]

corners1 = [
    [2372, 710],
    [3200, 1661],
    [397, 2303],
    [220, 1055]
]

corners2 = [

]

corners3 = [
    [2170, 1008],
    [3335, 1888],
    [932, 3359],
    [173, 1939]
]

corners = [corners0, corners1, corners2, corners3]

photo_ind = 3
img = cv.imread(paths[photo_ind])
img = img[:, :, ::-1]

paper_2d_corners = np.array(corners[photo_ind])

for i in range(4):
    plt.subplot(2,2,i+1)
    plt.imshow(img)

    paper_2d_corners = paper_2d_corners.tolist()
    paper_2d_corners.append(paper_2d_corners.pop(0))

    paper_2d_corners = np.array(paper_2d_corners, dtype=np.float32)


    paper_3d_corners = [
        [0, 0, 0],
        [21, 0, 0],
        [21, 29.7, 0],
        [0, 29.7, 0]
    ]
    paper_3d_corners = np.array(paper_3d_corners, dtype=np.float32)

    rmse, cam_mtx, dist, rvec, tvec = calibrate(paper_3d_corners, paper_2d_corners)
    print(rmse)
    print(cam_mtx)
    print(dist)

    points_project = [
        [[x, 0, 0] for x in np.linspace(0, 21, 15)] +
        [[21, y, 0] for y in np.linspace(0, 29.7, 15)] +
        [[x, 29.7, 0] for x in np.linspace(21, 0, 15)] +
        [[0, y, 0] for y in np.linspace(29.7, 0, 15)] +
        [[x, 29.7/2, 0] for x in np.linspace(0, 21, 15)] +
        [[21/2, y, 0] for y in np.linspace(0, 29.7, 15)]
    ][0]
    points_project = np.array(points_project)

    points_border_img, _ = cv.projectPoints(points_project, rvec, tvec, cam_mtx, dist)

    points_border_img = points_border_img.reshape(-1, 2)

    for x, y in points_border_img:
        plt.plot(x, y, "og", markersize=10)

    # plt.subplot(1,2,2)
    # straight = paper_straight_on(img, paper_2d_corners, 500)
    # plt.imshow(straight)
    # plt.show()

    # paper_pointcloud(img, paper_2d_corners, 500)

plt.show()