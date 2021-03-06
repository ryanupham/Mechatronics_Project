import time

from PIL import Image

from lines import intersection, hough_lines, find_triangles
from points import thin, hough, hough_points, trim_close_points


def color_match(c1, c2, tol):
    # r1 = c1 & 0xFF
    # g1 = c1 >> 16 & 0xFF
    # b1 = c1 >> 24 & 0xFF
    #
    # r2 = c2 & 0xFF
    # g2 = c2 >> 16 & 0xFF
    # b2 = c2 >> 24 & 0xFF

    return ((c2[0] - c1[0]) ** 2 + (c2[1] - c1[1]) ** 2 + (c2[2] - c1[2]) ** 2) ** 0.5 <= tol


def find_colors_tolerance(img, col, tol):
    width, height = img.size
    pixels = img.load()

    matches = []

    for y in range(height):
        for x in range(width):
            pix_col = pixels[x, y]
            if color_match(col, pix_col, tol):
                matches.append((x, y))

    return matches

img = Image.open("./images/signs.jpg")
img_pixels = img.load()

start = time.time()
matches = find_colors_tolerance(img, (214, 69, 66), 20)
print(time.time() - start)

start = time.time()
matches = thin(matches)
print(time.time() - start)

for match in matches:
    img_pixels[match] = 0

img.save("thin.bmp")

start = time.time()
accum = hough(matches)
print(time.time() - start)

h = Image.new("RGB", (len(accum[0]), len(accum)), "black")
hough_pixels = h.load()

for y, line in enumerate(accum):
    for x, intensity in enumerate(line):
        hough_pixels[x, y] = (intensity * 2, intensity * 2, intensity * 2)

start = time.time()
hp = hough_points(accum)
print(time.time() - start)

h.save("hough.bmp")

lines = hough_lines(hp)

for line in lines:
    for x in range(img.size[0]):
        y = line[0] * x + line[1]

        if 0 <= x < img.size[0] and 0 <= y < img.size[1]:
            img_pixels[x, y] = (0, 0, 255)

intersections = []

for ind, line1 in enumerate(lines[:-1]):
    for line2 in lines[ind + 1:]:
        p = intersection(line1, line2)

        if p is not None:
            intersections.append(p)

intersections = [(x, y) for x, y in intersections if 0 <= x < img.size[0] and 0 <= y < img.size[1]]

for x, y in intersections:
    for tx in range(-1, 2):
        for ty in range(-1, 2):
            img_pixels[x + tx, y + ty] = (255, 255, 255)

triangles = find_triangles(intersections)
trim_close_points(triangles)

for x, y, size in triangles:
    for tx in range(-2, 3):
        for ty in range(-2, 3):
            img_pixels[x + tx, y + ty] = (50, 200, 50)

img.save("hough_lines.bmp")
