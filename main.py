import math

import numpy as np
from PIL import Image, ImageColor


def rgb_to_hex(r, g, b):
    return '{:02x}{:02x}{:02x}'.format(r, g, b)


def decode():
    while True:
        input_file = input(
            'Enter the image name (with extension) of the image you wish to '
            'open: '
        )
        try:
            img = Image.open(input_file)
            break
        except OSError:
            print('Invalid file. Try again.')
    data = np.asarray(img)
    file_data = ''
    for row in data:
        for pixel in row:
            file_data += rgb_to_hex(pixel[0], pixel[1], pixel[2])

    output_file = input(
        'Enter the filename (with extension) of the file you wish to save: '
    )
    with open(output_file, "wb") as f:
        f.write(bytes.fromhex(file_data))


def encode():
    colors = []
    while True:
        input_file = input(
            'Enter the filename (with extension) of the file you wish to '
            'open: '
        )
        try:
            with open(input_file, 'rb') as f:
                color = ''
                while True:
                    data = f.read(1)
                    if not data:
                        break
                    if len(color) == 6:
                        colors.append('#' + color)
                        color = data.hex()
                    else:
                        color += data.hex()
            if color != '':
                while len(color) < 6:
                    color += '0'
                colors.append('#' + color)
            break
        except OSError:
            print('Invalid file. Try again.')

    size = len(colors)
    root = math.ceil(math.sqrt(size))
    x, y = 1, size
    for i in range(root + 1, 1, -1):
        if size % i == 0:
            x, y = i, size / i
            break

    image_data = []
    image_row = []
    for color in colors:
        image_row.append(list(ImageColor.getcolor(color, 'RGB')))
        if len(image_row) == x:
            image_data.append(image_row)
            image_row = []

    output_file = input(
        'Enter the name (without extension) of the image file you wish to '
        'save: '
    )
    img = Image.fromarray((np.array(image_data)).astype(np.uint8))
    img.save(output_file + '.png')


if __name__ == '__main__':
    while True:
        mode = input('(E)ncode or (D)ecode? ').lower()
        if mode in ['e', 'encode', '1']:
            encode()
            break
        elif mode in ['d', 'decode', '2']:
            decode()
            break
