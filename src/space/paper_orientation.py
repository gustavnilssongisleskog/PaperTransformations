import numpy as np
import cv2 as cv
from src.space.matrices import calibrate
from src.space.straight_paper import paper_corners_3d
"""
def line(a, b) -> tuple:
    return (b[1] - a[1]), (a[0] - b[0]), (a[1] * b[0] - a[0] * b[1])


def sqr_distance_points_to_line(points: np.ndarray, a, b, c) -> float:
    return np.sum((a * points[:, 0] + b * points[:, 1] + c) ** 2) / (a ** 2 + b ** 2)
    
    
def orientation_quality(paper_corners_2d: np.ndarray) -> tuple:
    paper_corners_2d = np.array(paper_corners_2d)
    rmse, cam_mtx, dist, rvec, tvec = calibrate(paper_corners_3d, paper_corners_2d)
    
    num_edge = 300
    paper_border_3d = (
        [[x, 0, 0] for x in np.linspace(0, 21, num_edge)],
        [[21, y, 0] for y in np.linspace(0, 29.7, num_edge)],
        [[x, 29.7, 0] for x in np.linspace(21, 0, num_edge)],
        [[0, y, 0] for y in np.linspace(29.7, 0, num_edge)]
    )
    
    sum_dist = 0
    for i in range(4):
        paper_edge, _ = cv.projectPoints(np.array(paper_border_3d[i]), rvec, tvec, cam_mtx, dist)
        paper_edge = paper_edge.reshape(-1, 2)
        
        p1 = paper_corners_2d[i]
        p2 = paper_corners_2d[(i + 1) % 4]
        a, b, c = line(p1, p2)
        sum_dist += sqr_distance_points_to_line(paper_edge, a, b, c)
    
    return sum_dist, cam_mtx, dist, rvec, tvec, paper_corners_2d
    
    
def best_orientation(corners: list) -> tuple:    
    sum_dist, cam_mtx, dist, rvec, tvec, paper_corners_2d = min(
        orientation_quality(np.array(corners)),
        orientation_quality(np.array(corners[1:] + corners[:1]))
    )
    
    return cam_mtx, dist, rvec, tvec, paper_corners_2d
"""

def best_orientation(corners: np.ndarray) -> tuple:
    # assumes corners are given in clockwise order
    
    _, top_left = min([(np.sum((corners[i] - corners[(i + 1) % 4]) ** 2), i) for i in range(4)])
    
    oriented_corners = np.empty((4, 2), dtype=np.float32)
    oriented_corners[:4 - top_left] = corners[top_left:]
    oriented_corners[4 - top_left:] = corners[:top_left]
    
    _, cam_mtx, dist, rvec, tvec = calibrate(paper_corners_3d, oriented_corners)
    
    return cam_mtx, dist, rvec, tvec, oriented_corners
    