from collections import deque
from numpy import ndarray
from src.regions.polygons import approximates_quadrilateral


def all_regions(img: ndarray) -> list:
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
                
    regions = [set((x, y) for (y, x) in reg) for reg in regions]
    return regions

def quadrilateral_regions(img: ndarray, tolerance: float=0.1) -> list:
    regions = all_regions(img)

    width, height = img.shape

    good_regions = []
    for region in regions:

        # dont count regions touching the edge!
        max_x, max_y, min_x, min_y = 0, 0, width, height
        for p in region:
            max_x = max(max_x, p[0])
            max_y = max(max_y, p[1])
            min_x = min(min_x, p[0])
            min_y = min(min_y, p[1])
        if max_x == width - 1 or max_y == height - 1 or min_x == 0 or min_y == 0:
            continue

        does_approximate, quad_area, quad_points = approximates_quadrilateral(list(region), tolerance)

        if not does_approximate:
            continue

        if quad_area < width * height / 50:
            continue

        good_regions.append(quad_points)

    return good_regions



def main():
    from src.image_processing.binarization import otsu_gauss, grayscale
    from src.regions.polygons import maximal_quadrilateral, convex_hull
    import cv2 as cv
    from matplotlib import pyplot as plt

    img = cv.imread("C:/Users/ggisl/Desktop/PaperTransformations/images/IMG_03.jpg")[:,:,::-1]
    width = int(img.shape[1] / 4)
    height = int(img.shape[0] / 4)
    dim = (width, height)
    
    # resize image
    img = cv.resize(img, dim, interpolation=cv.INTER_AREA)
    thresh = otsu_gauss(img)

    plt.subplot(1,2,1)
    plt.imshow(thresh)


    quads = quadrilateral_regions(thresh)

    # print(thresh.shape[0] * thresh.shape[1])
    # reg = all_regions(thresh)

    # hulls = [convex_hull(list(region)) for region in reg]
    # quads = [maximal_quadrilateral(hull) for hull in hulls]
    plt.subplot(1,2,2)
    plt.imshow(grayscale(img))

    print(quads)
    for hull in quads:
        for x, y in hull:
            plt.plot(x, y, "og", markersize=10)

    plt.show()

if __name__ == "__main__":
    main()