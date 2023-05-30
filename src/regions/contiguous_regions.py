from collections import deque
from  numpy import ndarray


def all_regions(img: ndarray):
    assert len(img.shape) == 2

    regions = []

    h, w = img.shape

    vis = set()
    q = deque()

    for i in range(h):
        for j in range(w):

            if img[i, j] == 0 or (i, j) in vis:
                continue

            new_reg = set()
            new_reg.add((i, j))
            q.append((i, j))

            while q:
                node_i, node_j = q.popleft()

                neighbors = [(node_i - 1, node_j), (node_i + 1, node_j), (node_i, node_j - 1), (node_i, node_j + 1)]
                neighbors = filter(lambda tup: 0 <= tup[0] < h and 0 <= tup[1] < w and img[tup] and tup not in new_reg, neighbors)

                for n in neighbors:
                    q.append(n)
                    new_reg.add(n)

            regions.append(new_reg)
            for p in new_reg:
                vis.add(p)

    return regions



def main():
    from src.image_processing.binarization import otsu_gauss
    import cv2 as cv

    img = cv.imread("C:/Users/ggisl/Desktop/PaperTransformations/images/IMG_03.jpg")[:,:,::-1]
    thresh = otsu_gauss(img)

    print(thresh.shape[0] * thresh.shape[1])
    reg = all_regions(thresh)

    s = sum(map(len, reg))
    print(s)
    print(thresh.sum() // 255)

if __name__ == "__main__":
    main()