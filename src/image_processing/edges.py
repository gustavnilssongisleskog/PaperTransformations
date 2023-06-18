import numpy as np
import cv2 as cv
from numpy import ndarray


def highpass(img: ndarray, n: int) -> ndarray:
    assert len(img.shape) == 2
    assert n % 2 == 1 and n > 1

    kernel = np.ones((n, n), dtype=np.float32) / n ** 2
    gauss = cv.filter2D(np.array(img, dtype=np.float32),-1,kernel)
    sharp = img - gauss

    return sharp

def erode(img: ndarray, erosion_size: int=1) -> ndarray:
    erosion_shape = cv.MORPH_RECT
    element = cv.getStructuringElement(erosion_shape, (2 * erosion_size + 1, 2 * erosion_size + 1), (erosion_size, erosion_size))

    return cv.erode(img, element)

def dilate(img: ndarray, dilate_size: int=1) -> ndarray:
    dilate_shape = cv.MORPH_RECT
    element = cv.getStructuringElement(dilate_shape, (2 * dilate_size + 1, 2 * dilate_size + 1), (dilate_size, dilate_size))

    return cv.dilate(img, element)

def remove_paper_edge(img: ndarray, n: int, erosion_size: int=1, dilate_size: int=2) -> ndarray:
    filtered = highpass(img, n)
    eroded = erode(filtered, erosion_size)
    dilated = dilate(eroded, dilate_size)

    edges = (dilated > 150) * 255

    return np.minimum(img, 255 - edges)



def main():
    from src.image_processing.binarization import otsu_gauss, grayscale
    from matplotlib import pyplot as plt
    for i in range(8,10):
        
        img = cv.imread(f"C:/Users/ggisl/Desktop/PaperTransformations/images/IMG_0{i}.jpg")[:,:,::-1]
        width = int(img.shape[1])# / 4)
        height = int(img.shape[0])# / 4)
        dim = (width, height)

        small = cv.resize(img, dim, interpolation=cv.INTER_AREA)

        gray = grayscale(small)
        plt.subplot(1,4,1)
        plt.imshow(small)

        n = 45
        erode_size = 1
        dilate_size = 2

        edge = highpass(gray, n)
        #edge = erode(edge, erode_size)
        #edge = dilate(edge, dilate_size)

        plt.subplot(1,4,2)
        plt.imshow(edge)
        edge = np.array(edge < -3, dtype=np.uint8) * 255

        closed = dilate(edge, 4)
        closed = erode(closed, 4)


        #removed_edges = np.array(remove_paper_edge(gray, n, erode_size, dilate_size), dtype=np.uint8)
        

        strong_edges = 255 - closed
        plt.subplot(1,4,3)
        plt.imshow(strong_edges)

        zero_on_non_edges = np.minimum(gray, strong_edges)
        thresh = otsu_gauss(zero_on_non_edges)
        # thresh = otsu_gauss(removed_edges)

        plt.subplot(1,4,4)
        plt.imshow(zero_on_non_edges)

        print((thresh == strong_edges).all())

        plt.show()

if __name__ == "__main__":
    main()