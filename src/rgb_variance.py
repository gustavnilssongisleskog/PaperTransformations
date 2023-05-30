import numpy as np
import cv2 as cv
from numpy import ndarray

def rgb_std(img: ndarray) -> ndarray:
    assert len(img.shape) == 3

    return np.std(img, axis=2)

def relative_rgb_std(img: ndarray) -> ndarray:
    assert len(img.shape) == 3

    return rgb_std(img) / (np.mean(img, axis=2) + 1)

"""
def main():
    from matplotlib import pyplot as plt

    #img = cv.imread("C:/Users/ggisl/Desktop/Parking/images/personbil.jpg")
    img = cv.imread("C:/Users/ggisl/Desktop/PaperTransformations/images/IMG_03.jpg")
    img = img[:, :, ::-1]

    rel_std = relative_rgb_std(img)
    std = rgb_std(img)
    thresh = otsu_gauss(img)
    gray = grayscale(img)

    #std = np.array(std * 255 / np.max(std), dtype=np.uint8)

    threshed_std = 255 - otsu_gauss(np.array(std, dtype=np.uint8))

    imgs = [gray, thresh, std,  rel_std]
    for i in range(4):
        plt.subplot(2,2,i+1)
        plt.imshow(imgs[i])

    plt.show()

    comb = threshed_std * thresh
    corners = good_corners(comb)
    plt.imshow(comb)

    for x, y in corners:
        plt.plot(x, y, "og", markersize=10)
    plt.show()



if __name__ == "__main__":
    main()

"""