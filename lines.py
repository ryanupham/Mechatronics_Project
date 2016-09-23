from math import cos, radians, sin

from points import distance


def hough_lines(points):
    lines = []

    for point in points:
        theta, r = point
        px, py = cos(radians(theta)) * r, sin(radians(theta)) * r
        m = sin(radians(theta + 90)) / cos(radians(theta + 90))
        b = py - m * px

        lines.append((m, b))

    return lines


def intersection(l1, l2):
    if l1[0] == l2[0]:
        return None

    x = (l2[1] - l1[1]) / (l1[0] - l2[0])
    y = l1[0] * x + l1[1]

    return x, y


def find_triangles(points, min_size=30, threshold=0.1):
    triangles = []

    for ind1, p1 in enumerate(points[:-2]):
        for ind2, p2 in enumerate(points[ind1 + 1:-1], ind1 + 1):
            dist1 = distance(p1, p2)

            if dist1 + dist1 * threshold < min_size:
                continue

            for p3 in points[ind2 + 1:]:
                dist2, dist3 = distance(p1, p3), distance(p2, p3)
                avg_dist = sum([dist1, dist2, dist3]) / 3

                e1, e2, e3 = abs(dist1 - dist2), abs(dist1 - dist3), abs(dist2 - dist3)
                acceptable_error = avg_dist * threshold

                if e1 <= acceptable_error and e2 <= acceptable_error and e3 <= acceptable_error:
                    cx = sum([p[0] for p in [p1, p2, p3]]) / 3
                    cy = sum([p[1] for p in [p1, p2, p3]]) / 3

                    triangles.append((cx, cy, avg_dist))

    return triangles
