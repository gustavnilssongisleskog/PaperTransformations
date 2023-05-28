import numpy as np
import cv2 as cv
from numpy import ndarray
from math import sqrt
from binarization import otsu_gauss, grayscale, adaptive_mean, adaptive_gauss

def good_corners(img: ndarray) -> ndarray:
    gray = grayscale(img)
    diag = sqrt(np.sum(np.array(img.shape) ** 2))

    corners = cv.goodFeaturesToTrack(gray, 20, 0.1, diag / 1000)
    corners = corners.reshape(-1, 2)
    corners = np.array(corners, dtype=np.int64)
    
    return corners




def main():
    from matplotlib import pyplot as plt
    paths = [f"C:/Users/ggisl/Desktop/PaperTransformations/images/IMG_0{i}.jpg" for i in range(4)]
    photo_ind = 3
    img = cv.imread(paths[photo_ind])
    img = img[:, :, ::-1]

    thresh = adaptive_gauss(img)
    thresh = cv.GaussianBlur(thresh,(49,49),0)
    gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    plt.subplot(1,2,1)
    plt.imshow(gray)

    corners = good_corners(thresh)

    plt.subplot(1,2,2)
    plt.imshow(thresh)
    

    for x, y in corners:
        plt.plot(x, y, "og", markersize=10)

    plt.show()




if __name__ == "__main__":
    main()
