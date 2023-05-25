import cv2 as cv
import numpy as np
from numpy import ndarray
from typing import Tuple
from matrices import *
from matplotlib import pyplot as plt

num_photos = 2

paths = [f"C:/Users/ggisl/Desktop/RotatingPapers/images/IMG_0{i}.jpg" for i in range(num_photos)]
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

corners = [corners0, corners1, corners2]

for i in range(num_photos):
    img = cv.imread(paths[i])
    img = img[:, :, ::-1]
    plt.subplot(1, num_photos, i + 1)
    plt.imshow(img)



    paper_2d_corners = np.array(corners[i], dtype=np.float32)


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
    points_project = np.array(points_project, dtype=np.float32)

    points_border_img, _ = cv.projectPoints(points_project, rvec, tvec, cam_mtx, dist)
    points_border_img = points_border_img.reshape(-1, 2)

    for x, y in points_border_img:
        plt.plot(x, y, "og", markersize=10)


plt.show()