from typing import Tuple

def convex_hull(points: list) -> list:
    def cross(p1, p2, p3):
        return 0

    return []

def shoelace(hull: list) -> float:
    return 0

def maximal_quadrilateral(hull: list) -> Tuple[float, list]:
    return 0, []

def approximates_quadrilateral(points: list, tolerance: float) -> Tuple[bool, list]:
    hull = convex_hull(points)
    hull_area = shoelace(hull)

    quad_area, quad = maximal_quadrilateral(hull)

    return abs(hull_area - quad_area) / hull_area < tolerance, quad
