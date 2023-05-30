import numpy as np
import cv2 as cv
from numpy import ndarray

from src.image_processing.rgb_variance import rgb_std, relative_rgb_std

def grayscale(img: ndarray) -> ndarray:
    if len(img.shape) == 2:
        return img
    
    return cv.cvtColor(img, cv.COLOR_RGB2GRAY)


def otsu_gauss(img: ndarray) -> ndarray:
    gray = grayscale(img)
    
    blur = cv.GaussianBlur(gray,(5,5),0)
    _, thresh = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)

    return thresh


def adaptive_mean(img: ndarray) -> ndarray:
    gray = grayscale(img)
    thresh = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 2)

    return thresh

def adaptive_gauss(img: ndarray) -> ndarray:
    gray = grayscale(img)
    thresh = cv.adaptiveThreshold(gray,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 101, 2)

    return thresh

def median_blur(img: ndarray, ksize: int = 5) -> ndarray:
    gray = grayscale(img)

    return cv.medianBlur(gray, ksize)



def binarize_white_only(img: ndarray, variance_tolerance: float=10, thresh_func=otsu_gauss) -> ndarray:
    std = rgb_std(img)
    white_pixels = std < variance_tolerance

    thresh_light = thresh_func(img)

    return thresh_light * white_pixels


def main():
    from matplotlib import pyplot as plt
    paths = [f"C:/Users/ggisl/Desktop/PaperTransformations/images/IMG_0{i}.jpg" for i in range(4)]
    photo_ind = 3
    for photo_ind in range(4):
        img = cv.imread(paths[photo_ind])
        img = img[:, :, ::-1]
        gray = grayscale(img)

        plt.subplot(2,2,1)
        plt.imshow(img)

        otsu = otsu_gauss(gray)

        plt.subplot(2,2,2)
        plt.imshow(otsu)

        std = rgb_std(img)
        plt.subplot(2,2,3)
        plt.imshow(std)

        white = binarize_white_only(img)
        plt.subplot(2,2,4)
        plt.imshow(white)

        plt.show()

if __name__ == "__main__":
    main()
