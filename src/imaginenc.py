#!/usr/bin/env python3

import math
import sys
import argparse
from typing import List, Optional, Dict, Iterable, Union, Any

import numpy as np
from PIL import Image, ImageColor

META_SIZE = 6
META_INFO = {
    'meta_size': (0, 3, int),
    'extra_zeros': (3, 4, int)
}


def parse_meta(data: bytes) -> Dict[str, Any]:
    bytes_converters = {
        int: bytes_to_int,
        str: bytes_to_str
    }
    meta = {}
    for key, (fr, to, type_) in META_INFO.items():
        meta[key] = bytes_converters[type_](data[fr: to])
    return meta


def decode_image_to_bytes(
        image: Union[Iterable[np.uint8], Image.Image]) -> bytes:
    data = bytes(list(np.asarray(image, dtype=np.uint8).flatten()))
    meta = parse_meta(data)
    file_data_hex = ''.join(
        f'{pixel:02x}' for pixel in data[meta['meta_size']:]
    )
    return bytes.fromhex(
        file_data_hex[:len(file_data_hex) - meta['extra_zeros'] * 2]
    )


def decode_image_name(input_file_name: str, output_file_name: str):
    try:
        if not input_file_name.endswith('.png'):
            input_file_name += '.png'
        image = Image.open(input_file_name)
    except OSError:
        print('Invalid file.')
        return
    file_bytes = decode_image_to_bytes(image)
    with open(output_file_name, 'wb') as f:
        f.write(file_bytes)


def int_to_bytes(num: int, num_bytes: int, signed: bool = False) -> bytes:
    return num.to_bytes(num_bytes, byteorder='big', signed=signed)


def bytes_to_int(bytes_: bytes, signed: bool = False) -> int:
    return int.from_bytes(bytes_, 'big', signed=signed)


def str_to_bytes(string: str) -> bytes:
    return string.encode('ASCII')


def bytes_to_str(bytes_: bytes) -> str:
    return bytes_.decode('ASCII')


def bytes_to_hex(bytes_: bytes) -> List[str]:
    return list(map(lambda b: f'{b:02x}', bytes_))


def int_to_n_hex(num: int, num_hex: int) -> List[str]:
    return bytes_to_hex(int_to_bytes(num, num_hex))


def colors_to_image(colors: List[str]) -> Image.Image:
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
    image = Image.fromarray((np.array(image_data)).astype(np.uint8))
    return image


def encode_bytes_to_colors(input_file_bytes: bytes) -> List[str]:
    input_file_hex = bytes_to_hex(input_file_bytes)
    extra_zeros = -len(input_file_hex) % 3
    meta_hex = [
        *int_to_n_hex(META_SIZE, 3),
        *int_to_n_hex(extra_zeros, 1)
    ]
    meta_hex += int_to_n_hex(0, META_SIZE - len(meta_hex))
    colors = []
    color = '#'
    for byte_hex in meta_hex + input_file_hex:
        color += byte_hex
        if len(color) == 7:
            colors.append(color)
            color = '#'
    if color != '#':
        while len(color) < 7:
            color += '0'
        colors.append(color)
    return colors


def get_file_bytes(input_file_name: str) -> Optional[bytes]:
    try:
        with open(input_file_name, 'rb') as f:
            return f.read()
    except OSError:
        return None


def encode_file_name(input_file_name: str, output_file_name: str):
    input_file_bytes = get_file_bytes(input_file_name)
    if input_file_bytes is None:
        print('Invalid file.')
        return
    colors = encode_bytes_to_colors(input_file_bytes)
    image = colors_to_image(colors)
    if not output_file_name.endswith('.png'):
        output_file_name += '.png'
    image.save(output_file_name)


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
        encode_file_name(args['input'], args['output'])
    elif args['mode'] == 'd':
        decode_image_name(args['input'], args['output'])


if __name__ == '__main__':
    main()
