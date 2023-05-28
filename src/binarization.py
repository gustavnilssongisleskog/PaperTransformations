import numpy as np
import cv2 as cv
from numpy import ndarray

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




def main():
    from matplotlib import pyplot as plt
    paths = [f"C:/Users/ggisl/Desktop/PaperTransformations/images/IMG_0{i}.jpg" for i in range(4)]
    photo_ind = 3
    img = cv.imread(paths[photo_ind])
    img = img[:, :, ::-1]
    gray = grayscale(img)

    img = cv.imread("C:/Users/ggisl/Desktop/Parking/images/personbil.jpg")
    img = img[:, :, ::-1]

    plt.imshow(img)
    plt.show()

    plt.subplot(2,2,1)
    plt.imshow(gray)

    otsu = otsu_gauss(gray)

    plt.subplot(2,2,2)
    plt.imshow(otsu)

    median = median_blur(gray)
    plt.subplot(2,2,3)
    plt.imshow(median)

    otsu_median = median_blur(otsu, 35)
    plt.subplot(2,2,4)
    plt.imshow(otsu_median)

    plt.show()

if __name__ == "__main__":
    main()
