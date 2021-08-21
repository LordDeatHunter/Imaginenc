#!/usr/bin/env python3

import math
import sys
import argparse
from typing import List, Optional, Dict

import numpy as np
from PIL import Image, ImageColor


def rgb_to_hex(r: np.uint8, g: np.uint8, b: np.uint8) -> str:
    return f'{r:02x}{g:02x}{b:02x}'


def decode(input_file_name: str, output_file_name: str):
    try:
        if not input_file_name.endswith('.png'):
            input_file_name += '.png'
        img = Image.open(input_file_name)
    except OSError:
        print('Invalid file.')
        return

    data = np.asarray(img)
    file_data = []
    for row in data:
        for pixel in row:
            file_data.append(rgb_to_hex(pixel[0], pixel[1], pixel[2]))

    with open(output_file_name, 'wb') as f:
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


def write_colors_to_image(colors: List[str], output_file_name: str):
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
    img = Image.fromarray((np.array(image_data)).astype(np.uint8))
    if not output_file_name.endswith('.png'):
        output_file_name += '.png'
    img.save(output_file_name)


def encode(input_file_name: str, output_file_name: str):
    colors = []
    file_bytes = get_file_bytes(input_file_name)
    if file_bytes is None:
        print('Invalid file.')
        return
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
    write_colors_to_image(colors, output_file_name)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Converts any file into an image,'
                    ' and images back to files.'
                    ' Run without args for interactive input mode.'
    )
    encode_decode_group = parser.add_mutually_exclusive_group(required=True)
    encode_decode_group.add_argument(
        '-e', '--encode',
        action='store_true',
        help='encode file to image'
    )
    encode_decode_group.add_argument(
        '-d', '--decode',
        action='store_true',
        help='decode image to file'
    )
    parser.add_argument(
        '-i', '--input',
        type=str,
        help='input file',
        required=True
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='output file',
        required=True
    )
    return parser.parse_args()


def process_args_interactive() -> Dict[str, str]:
    print("""
███████████████████████▀█████████████████████████████████
█▄─▄█▄─▀█▀─▄██▀▄─██─▄▄▄▄█▄─▄█▄─▀█▄─▄█▄─▄▄─█▄─▀█▄─▄█─▄▄▄─█
██─███─█▄█─███─▀─██─██▄─██─███─█▄▀─███─▄█▀██─█▄▀─██─███▀█
▀▄▄▄▀▄▄▄▀▄▄▄▀▄▄▀▄▄▀▄▄▄▄▄▀▄▄▄▀▄▄▄▀▀▄▄▀▄▄▄▄▄▀▄▄▄▀▀▄▄▀▄▄▄▄▄▀
    """)

    while (mode := input('(E)ncode or (D)ecode? ').lower()[0]) not in 'de':
        print('Invalid input.')

    if mode == 'e':
        input_file_name = input(
            'Enter the filename (with extension) of the file you wish to '
            'encode: '
        )
    else:
        input_file_name = input(
            'Enter the filename (without extension) of the image you wish to '
            'decode: '
        )

    if mode == 'e':
        output_file_name = input(
            'Enter the filename (without extension) of the image output file: '
        )
    else:
        output_file_name = input(
            'Enter the filename (with extension) of the decoded output file: '
        )

    return {
        'mode': mode,
        'input': input_file_name,
        'output': output_file_name
    }


def process_args() -> Dict[str, str]:
    if not len(sys.argv) > 1:
        return process_args_interactive()
    args = parse_args()
    return {
        'mode': 'd' if args.decode else 'e',
        'input': args.input,
        'output': args.output
    }


def main():
    args = process_args()
    if args['mode'] == 'e':
        encode(args['input'], args['output'])
    elif args['mode'] == 'd':
        decode(args['input'], args['output'])


if __name__ == '__main__':
    main()
