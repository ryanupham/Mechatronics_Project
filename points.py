from math import ceil, hypot


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

    accum = [[0 for x in range(0, width + 1)] for y in range(0, height + 1)]

    max_dist = hypot(width, height)
