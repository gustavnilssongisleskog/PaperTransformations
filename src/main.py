import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from space.matrices import calibrate_corners
from src.image_processing.edges import paper_edges
from src.regions.paper_regions import quadrilateral_regions
from src.regions.polygons import shoelace
from src.space.paper_orientation import best_orientation
from src.space.straight_paper import paper_straight_on
from src.space.intersections import intersection_coloring

def main():
    path = input("Enter path to image file:")
    img = cv.imread(path)
    if img is None:
        print("The path you entered does not lead to an image file")
        exit()
    
    img = img[:,:,::-1]
    
    width = img.shape[1]
    height = img.shape[0]
    
    area = width * height
    
    scale = 1 if area < 1e6 else np.sqrt(area / 1e6)

    scaled = cv.resize(img, (int(width / scale), int(height / scale)), interpolation=cv.INTER_AREA)
    
    n = 11
    erosion_size = 1
    dilate_size = 1
    
    print("\nFinding edges in image...")
    edges = paper_edges(scaled, n=n, erosion_size=erosion_size, dilate_size=dilate_size)
    
    print("Partitioning image regions...")
    quad_regions = quadrilateral_regions(edges)
    
    if len(quad_regions) == 0:
        print("Could not find a paper in the image")
        exit()
        
    
    corners = max(quad_regions, key=shoelace)
    corners = best_orientation(np.array(corners))
    corners *= scale
    
    plt.subplot(1,2,1)
    plt.imshow(img)
    
    for x, y in corners:
        plt.plot(x, y, "og", markersize=5)
    
    
    # _, cam_mtx, dist, rvec, tvec = calibrate_corners(corners)

    print("Simulating paper...")
    # straight = paper_straight_on(img, 2000, cam_mtx, dist, rvec, tvec)
    straight = intersection_coloring(img, corners, 500)
    plt.subplot(1,2,2)
    plt.imshow(straight)
    
    plt.show()

    
    
if __name__ == "__main__":
    main()