from math import ceil, hypot, cos, radians, sin


def distance(p1, p2):
    return ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5


def thin(points):
    width, height = 0, 0

    for point in points:
        if point[0] > width:
            width = point[0]
        if point[1] > height:
            height = point[1]

    width += 2
    height += 2

    pixels = [[False for x in range(0, width + 1)] for y in range(0, height + 1)]

    for point in points:
        pixels[point[1]][point[0]] = True

    check = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]

    trimmed = True

    c = 1

    while trimmed:
        trimmed = False

        flags = []

        for y in range(1, height - 1):
            for x in range(1, width - 1):
                if not pixels[y][x]:
                    continue

                count = 0
                trans = 0

                for i in range(len(check)):
                    if pixels[y + check[i][1]][x + check[i][0]]:
                        count += 1
                    if i > 0:
                        if pixels[y + check[i][1]][x + check[i][0]] != pixels[y + check[i - 1][1]][x + check[i - 1][0]]:
                            trans += 1

                if 2 <= count <= 6:
                    if ceil(trans / 2.0) == 1:
                        if pixels[y + check[4][1]][x + check[4][0]] == False or \
                           pixels[y + check[2][1]][x + check[2][0]] == False or \
                           (pixels[y + check[0][1]][x + check[0][0]] == False and
                           (pixels[y + check[2][1]][x + check[2][0]] == False or
                           pixels[y + check[6][1]][x + check[6][0]] == False)):
                            flags.append((x, y))
                            trimmed = True

        for ind in flags:
            pixels[ind[1]][ind[0]] = False

        flags = []

        for y in range(1, height - 1):
            for x in range(1, width - 1):
                if not pixels[y][x]:
                    continue

                count = 0
                trans = 0

                for i in range(len(check)):
                    if pixels[y + check[i][1]][x + check[i][0]]:
                        count += 1
                    if i > 0:
                        if pixels[y + check[i][1]][x + check[i][0]] != pixels[y + check[i - 1][1]][x + check[i - 1][0]]:
                            trans += 1

                if 2 <= count <= 6:
                    if ceil(trans / 2.0) == 1:
                        if pixels[y + check[0][1]][x + check[0][0]] == False or \
                           pixels[y + check[6][1]][x + check[6][0]] == False or \
                           (pixels[y + check[4][1]][x + check[4][0]] == False and
                           (pixels[y + check[2][1]][x + check[2][0]] == False or
                           pixels[y + check[6][1]][x + check[6][0]] == False)):
                            flags.append((x, y))
                            trimmed = True

        for ind in flags:
            pixels[ind[1]][ind[0]] = False

    thinned_points = []

    for y in range(height):
        for x in range(width):
            if pixels[y][x]:
                thinned_points.append((x, y))

    return thinned_points


def hough(points):
    width, height = 0, 0

    for point in points:
        if point[0] > width:
            width = point[0]
        if point[1] > height:
            height = point[1]

    max_dist = ceil(hypot(width, height))
    accum = [[0 for x in range(-90, 90)] for y in range(-max_dist, max_dist + 1)]

    for point in points:
        for theta in range(-90, 90):
            r = round(point[0] * cos(radians(theta)) + point[1] * sin(radians(theta)))
            accum[r + max_dist][theta + 90] += 1

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
