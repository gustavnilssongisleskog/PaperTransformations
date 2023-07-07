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

    return list(reversed(top + bot))

def shoelace(hull: list) -> float:
    area = 0

    for i in range(len(hull) - 1):
        area += hull[i][0] * hull[i + 1][1] - hull[i + 1][0] * hull[i][1]
    area += hull[-1][0] * hull[0][1] - hull[0][0] * hull[-1][1]

    area /= 2

    return abs(area)

def maximal_quadrilateral(hull: list) -> Tuple[float, list]:
    # https://open.kattis.com/problems/citadelconstruction !!!
    # seems to be very difficult to get within the time limit with python though :(
    n = len(hull)

    best_area = 0
    best_hull = []

    for i in range(n):
        for j in range(i + 2, n):
            # ternary search between i and j for best triangle

            lo = i
            hi = j
            triangle1 = (0, (0, 0))
            while hi - lo > 5:

                mid1 = lo + (hi - lo) // 3
                area1 = shoelace([hull[i], hull[mid1], hull[j]])
                mid2 = hi - (hi - lo) // 3
                area2 = shoelace([hull[i], hull[mid2], hull[j]])

                if area1 > area2:
                    hi = mid2
                else:
                    lo = mid1
            for k in range(lo, hi + 1):
                triangle1 = max(triangle1, (shoelace([hull[i], hull[k], hull[j]]), hull[k]))

            # ternary search between j and "i + n" for best triangle
            lo = j
            hi = i + n
            triangle2 = (0, (0, 0))
            while hi - lo > 5:

                mid1 = lo + (hi - lo) // 3
                area1 = shoelace([hull[i], hull[mid1 % n], hull[j]])
                mid2 = hi - (hi - lo) // 3
                area2 = shoelace([hull[i], hull[mid2 % n], hull[j]])

                if area1 > area2:
                    hi = mid2
                else:
                    lo = mid1
            
            for k in range(lo, hi + 1):
                triangle2 = max(triangle2, (shoelace([hull[i], hull[k % n], hull[j]]), hull[k % n]))

            if triangle1[0] + triangle2[0] > best_area:
                best_area = triangle1[0] + triangle2[0]
                best_hull = [hull[i], triangle1[1], hull[j], triangle2[1]]


    return best_area, best_hull

def approximates_quadrilateral(points: list, tolerance: float) -> Tuple[bool, float, list]:
    hull = convex_hull(points)

    if len(hull) < 4:
        return False, 0, []
    hull_area = shoelace(hull)

    quad_area, quad = maximal_quadrilateral(hull)
    
    return abs(hull_area - quad_area) / hull_area < tolerance, quad_area, quad
