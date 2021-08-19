import math
from typing import List, Optional

import numpy as np
from PIL import Image, ImageColor


def rgb_to_hex(r: np.uint8, g: np.uint8, b: np.uint8) -> str:
    return f'{r:02x}{g:02x}{b:b02x}'


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
    file_data = []
    for row in data:
        for pixel in row:
            file_data.append(rgb_to_hex(pixel[0], pixel[1], pixel[2]))

    output_file = input(
        'Enter the filename (with extension) of the file you wish to save: '
    )
    with open(output_file, 'wb') as f:
        f.write(bytes.fromhex(''.join(file_data)))


def get_file_bytes(input_file_name: str) -> Optional[List[bytes]]:
    file_bytes = []
    try:
        with open(input_file_name, 'rb') as f:
            while byte := f.read(1):
                file_bytes.append(byte)
        return file_bytes
    except OSError:
        return None


def write_colors_to_image(colors: List[str]):
    size = len(colors)
    root = math.ceil(math.sqrt(size))
    x = 1
    for i in range(root + 1, 1, -1):
        if size % i == 0:
            x = i
            break

    image_data = []
    image_row = []
    for color in colors:
        image_row.append(list(ImageColor.getcolor(color, 'RGB')))
        if len(image_row) == x:
            image_data.append(image_row)
            image_row = []

    output_file_name = input(
        'Enter the name (without extension) of the image file you wish to '
        'save: '
    )
    img = Image.fromarray((np.array(image_data)).astype(np.uint8))
    img.save(f'{output_file_name}.png')


def encode():
    colors = []
    while True:
        input_file_name = input(
            'Enter the filename (with extension) of the file you wish to '
            'open: '
        )
        file_bytes = get_file_bytes(input_file_name)
        if file_bytes is not None:
            break
        print('Invalid file. Try again.')

    color = '#'
    for byte in file_bytes:
        color += byte.hex()
        if len(color) == 7:
            colors.append(color)
            color = '#'
    if color != '#':
        while len(color) < 7:
            color += '0'
        colors.append(color)
    write_colors_to_image(colors)


def main():
    while True:
        mode = input('(E)ncode or (D)ecode? ').lower()
        if mode in ['e', 'encode', '1']:
            encode()
            break
        elif mode in ['d', 'decode', '2']:
            decode()
            break


if __name__ == '__main__':
    main()
