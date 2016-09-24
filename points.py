from itertools import product
from math import ceil, hypot, cos, radians, sin


def distance(p1, p2):
    return ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5


def thin(points):
    points = points[:]
    width, height = 0, 0

    for point in points:
        if point[0] > width:
            width = point[0]
        if point[1] > height:
            height = point[1]

    width += 2
    height += 2

    check = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]

    pixels = [[False for x in range(0, width + 1)] for y in range(0, height + 1)]
    marked = set()

    for x, y in points:
        pixels[y][x] = True

    for x, y in points:
        for tx, ty in check:
            if not pixels[y + ty][x + tx]:
                marked.add((x, y))
                break

    trimmed = True
    flags = []

    while trimmed:
        flags.clear()

        for x, y in marked:
            count = 0
            trans = 0

            if pixels[y - 1][x]:
                count += 1

            for i in range(1, 8):
                if pixels[y + check[i][1]][x + check[i][0]]:
                    count += 1
                    if not pixels[y + check[i - 1][1]][x + check[i - 1][0]]:
                        trans += 1
                elif pixels[y + check[i - 1][1]][x + check[i - 1][0]]:
                    trans += 1

            if (2 <= count <= 6) and (trans == 1 or trans == 2):
                if pixels[y + check[4][1]][x + check[4][0]] == False or \
                   pixels[y + check[2][1]][x + check[2][0]] == False or \
                   (pixels[y + check[0][1]][x + check[0][0]] == False and
                   (pixels[y + check[2][1]][x + check[2][0]] == False or
                   pixels[y + check[6][1]][x + check[6][0]] == False)):
                    flags.append((x, y))

        for x, y in flags:
            pixels[y][x] = False

        for x, y in flags:
            for tx, ty in check:
                if pixels[y + ty][x + tx]:
                    marked.add((x + tx, y + ty))

        trimmed = len(flags) > 0
        flags.clear()

        for x, y in marked:
            count = 0
            trans = 0

            if pixels[y - 1][x]:
                count += 1

            for i in range(1, 8):
                if pixels[y + check[i][1]][x + check[i][0]]:
                    count += 1
                    if not pixels[y + check[i - 1][1]][x + check[i - 1][0]]:
                        trans += 1
                elif pixels[y + check[i - 1][1]][x + check[i - 1][0]]:
                    trans += 1

            if (2 <= count <= 6) and (trans == 1 or trans == 2):
                if pixels[y + check[0][1]][x + check[0][0]] == False or \
                   pixels[y + check[6][1]][x + check[6][0]] == False or \
                   (pixels[y + check[4][1]][x + check[4][0]] == False and
                   (pixels[y + check[2][1]][x + check[2][0]] == False or
                   pixels[y + check[6][1]][x + check[6][0]] == False)):
                    flags.append((x, y))

        for x, y in flags:
            pixels[y][x] = False

        marked.clear()

        for x, y in flags:
            for tx, ty in check:
                if pixels[y + ty][x + tx]:
                    marked.add((x + tx, y + ty))

        trimmed = trimmed or len(flags) > 0

    thinned_points = []

    for y in range(height):
        for x in range(width):
            if pixels[y][x]:
                thinned_points.append((x, y))

    return thinned_points


def hough(points):
    sin_lookup = [sin(radians(theta)) for theta in range(-90, 90)]
    cos_lookup = [cos(radians(theta)) for theta in range(-90, 90)]

    width, height = 0, 0

    for x, y in points:
        if x > width:
            width = x
        if y > height:
            height = y

    max_dist = ceil(hypot(width, height))
    accum = [[0 for x in range(-90, 90)] for y in range(-max_dist, max_dist + 1)]

    for x, y in points:
        for theta in range(180):
            r = round(x * cos_lookup[theta] + y * sin_lookup[theta])
            accum[r + max_dist][theta] += 1

    return accum


def hough_points(accum, threshold=100):
    points = []

    for y in range(len(accum)):
        for x in range(len(accum[y])):
            if accum[y][x] >= threshold:
                for ty in range(-1, 2):
                    for tx in range(-1, 2):
                        if not (ty == 0 and tx == 0) and 0 <= x + tx < len(accum[y]) and 0 <= y + ty < len(accum):
                            if accum[y][x] <= accum[y + ty][x + tx]:
                                accum[y][x] = 0

                if accum[y][x] != 0:
                    points.append((x - 90, y - len(accum) // 2))

    return points


def trim_close_points(points, dist=7):
    ind = 0

    while ind < len(points):
        for p in points[ind + 1:]:
            if distance(points[ind], p) <= dist:
                points.remove(p)

        ind += 1
