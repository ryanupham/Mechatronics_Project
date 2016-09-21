import time
from PIL import Image

from points import thin


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

start = time.time()
matches = find_colors_tolerance(img, (214, 69, 66), 20)
print(time.time() - start)

start = time.time()
matches = thin(matches)
print(time.time() - start)

print(len(matches))

for match in matches:
    img.im.putpixel(match, 0)

img.save("test.bmp")
