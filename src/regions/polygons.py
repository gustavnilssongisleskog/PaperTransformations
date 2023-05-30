from typing import Tuple

def convex_hull(points: list) -> list:
    def clockwise(p1, p2, p3):
        u = (p1[0] - p2[0], p1[1] - p2[1])
        v = (p3[0] - p2[0], p3[1] - p2[1])

        return u[0] * v[1] - u[1] * v[0] > 0
    
    points = sorted(points)

    top = points[:2]

    for p in points[2:]:
        while len(top) >= 2 and not clockwise(top[-2], top[-1], p):

            if p == (0.5, 1):
                print("ok", top)
            top.pop()

        top.append(p)
    
    bot = points[:-3:-1]

    for p in points[-3::-1]:
        while len(bot) >= 2 and not clockwise(bot[-2], bot[-1], p):
            bot.pop()

        bot.append(p)

    top.pop()
    bot.pop()

    return top + bot

def shoelace(hull: list) -> float:
    area = 0

    for i in range(len(hull) - 1):
        area += hull[i][0] * hull[i + 1][1] - hull[i + 1][0] * hull[i][1]
    area += hull[-1][0] * hull[0][1] - hull[0][0] * hull[-1][1]

    area /= 2

    return abs(area)

def maximal_quadrilateral(hull: list) -> Tuple[float, list]:
    return 0, []

def approximates_quadrilateral(points: list, tolerance: float) -> Tuple[bool, list]:
    hull = convex_hull(points)
    hull_area = shoelace(hull)

    quad_area, quad = maximal_quadrilateral(hull)

    return abs(hull_area - quad_area) / hull_area < tolerance, quad
