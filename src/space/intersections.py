import numpy as np

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
    return -1 / (l1[0] * l2[1] - l2[0] * l1[1]) * np.array([[l2[1], -l1[1]], [-l2[0], l1[0]]]) @ np.array([l1[2], l2[2]])


def intersection_coloring(img: np.ndarray, paper_corners_2d: np.ndarray, img_width: int) -> np.ndarray:
    
    from matplotlib import pyplot as plt
    
    pixel_size = paper_width / img_width
    
    top_vanish = intersection_lines(line(paper_corners_2d[0], paper_corners_2d[3]), line(paper_corners_2d[1], paper_corners_2d[2]))
    side_vanish = intersection_lines(line(paper_corners_2d[0], paper_corners_2d[1]), line(paper_corners_2d[2], paper_corners_2d[3]))
    
    img_height = int(img_width * paper_height / paper_width)
    
    ret = np.ones((img_height + 1, img_width + 1, 3), dtype=np.uint8)
    
    def color_recursive(corners_2d: np.ndarray, corners_3d: np.ndarray):
        corners_2d = np.array(corners_2d, dtype=np.float64)
        
        dx, dy = corners_3d[2] - corners_3d[0]
        
        if pixel_size > dy:
            # color the pixels at corners_3d
            for i in range(4):
                ret[int(corners_3d[i, 1] / paper_height * img_height), int(corners_3d[i, 0] / paper_width * img_width)] = img[int(corners_2d[i, 1]), int(corners_2d[i, 0])]
                
            return
        
        # create the next recursive points
        center2d = intersection_lines(line(corners_2d[0], corners_2d[2]), line(corners_2d[1], corners_2d[3]))
        center3d = np.array([dx, dy]) / 2 + corners_3d[0]
        
        top2d = intersection_lines(line(corners_2d[0], corners_2d[1]), line(top_vanish, center2d))
        top3d = np.array([dx, 0]) / 2 + corners_3d[0]
        
        right2d = intersection_lines(line(corners_2d[1], corners_2d[2]), line(side_vanish, center2d))
        right3d = np.array([0, dy]) / 2 + corners_3d[1]
        
        bot2d = intersection_lines(line(corners_2d[2], corners_2d[3]), line(top_vanish, center2d))
        bot3d = np.array([dx, 0]) / 2 + corners_3d[3]
        
        left2d = intersection_lines(line(corners_2d[3], corners_2d[0]), line(side_vanish, center2d))
        left3d = np.array([0, dy]) / 2 + corners_3d[0]
        
        color_recursive(np.array([corners_2d[0], top2d, center2d, left2d]), np.array([corners_3d[0], top3d, center3d, left3d]))
        color_recursive(np.array([top2d, corners_2d[1], right2d, center2d]), np.array([top3d, corners_3d[1], right3d, center3d]))
        color_recursive(np.array([center2d, right2d, corners_2d[2], bot2d]), np.array([center3d, right3d, corners_3d[2], bot3d]))
        color_recursive(np.array([left2d, center2d, bot2d, corners_2d[3]]), np.array([left3d, center3d, bot3d, corners_3d[3]]))
        
    color_recursive(paper_corners_2d, real_paper_corners)
    
    return ret
    