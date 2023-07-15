import numpy as np
import cv2 as cv

paper_width = 21
paper_height = 29.7
real_paper_corners = np.array([
    [0, 0],
    [paper_width, 0],
    [paper_width, paper_height],
    [0, paper_height]
], dtype=np.float64)

def line(a, b) -> tuple:
    return (b[1] - a[1]), (a[0] - b[0]), (a[1] * b[0] - a[0] * b[1])


def intersection_lines(l1, l2) -> np.ndarray:
    # return np.array([l1[1] * l2[2] - l2[1] * l1[2], l1[2] * l2[0] - l2[2] * l1[0]]) / (l1[0] * l2[1] - l2[0] * l1[1])
    return -1 / (l1[0] * l2[1] - l2[0] * l1[1]) * np.array([[l2[1], -l1[1]], [-l2[0], l1[0]]]) @ np.array([l1[2], l2[2]])

    
def intersection_coloring(img: np.ndarray, paper_corners_2d: np.ndarray, img_width: int) -> np.ndarray:
    n = 2
    while n < img_width:
        n = 2 * n - 1
        
    img_width = n
    paper_corners_2d = np.array(paper_corners_2d, dtype=np.float64)

    
    points_2d = np.zeros((img_width, img_width, 2), dtype=np.float64)
    points_2d[0, 0] = paper_corners_2d[0]
    points_2d[0, -1] = paper_corners_2d[1]
    points_2d[-1, -1] = paper_corners_2d[2]
    points_2d[-1, 0] = paper_corners_2d[3]
    
    
    top_vanish = intersection_lines(line(paper_corners_2d[0], paper_corners_2d[3]), line(paper_corners_2d[1], paper_corners_2d[2]))
    side_vanish = intersection_lines(line(paper_corners_2d[0], paper_corners_2d[1]), line(paper_corners_2d[2], paper_corners_2d[3]))
    
    
    q = [(0, img_width - 1, img_width - 1, 0)]
    
    while len(q) > 0:
        top, right, bot, left = q.pop() 
        
        # create the next recursive points
        center2d = intersection_lines(line(points_2d[top, left], points_2d[bot, right]), line(points_2d[top, right], points_2d[bot, left]))
        points_2d[(top + bot) // 2, (left + right) // 2] = center2d
        
        if top == 0:
            top2d = intersection_lines(line(points_2d[top, left], points_2d[top, right]), line(top_vanish, center2d))
            points_2d[0, (left + right) // 2] = top2d
        
        if left == 0:
            left2d = intersection_lines(line(points_2d[bot, left], points_2d[top, left]), line(side_vanish, center2d))
            points_2d[(top + bot) // 2, 0] = left2d
        
        right2d = intersection_lines(line(points_2d[top, right], points_2d[bot, right]), line(side_vanish, center2d))
        points_2d[(top + bot) // 2, right] = right2d
        
        bot2d = intersection_lines(line(points_2d[bot, right], points_2d[bot, left]), line(top_vanish, center2d))
        points_2d[bot, (left + right) // 2] = bot2d
        
        if bot - top <= 2:
            continue
        
        q.append(((top + bot) // 2, right, bot, (left + right) // 2))
        
        q.append(((top + bot) // 2, (left + right) // 2, bot, left))
        
        q.append((top, right, (top + bot) // 2, (left + right) // 2))
        
        q.append((top, (left + right) // 2, (top + bot) // 2, left))
        
    
    ret = np.ones((img_width, img_width, 3), dtype=np.uint8)
    for i in range(img_width):
        for j in range(img_width):
            x, y = points_2d[i, j]
            ret[i, j] = img[int(y), int(x)]
    
    
    img_height = int(img_width * paper_height / paper_width)
    ret = cv.resize(ret, (img_width, img_height), interpolation=cv.INTER_AREA)
    
    return ret
