#!/usr/bin/env python3

import os
import math
import sys
import argparse
from typing import List, Optional, Dict, Iterable, Union

import numpy as np
from PIL import Image, ImageColor

METADATA_INFO = {
    'metadata_size': (0, 3, int),
    'extra_bytes': (3, 4, int),
    'sign': (4, 54, str),
    'file_name': (54, 310, str)
}
Metadata = Dict[str, any]


def parse_metadata(data: bytes) -> Metadata:
    bytes_converters = {
        int: bytes_to_int,
        str: bytes_to_str
    }
    metadata = {}
    for key, (fr, to, type_) in METADATA_INFO.items():
        val = bytes_converters[type_](data[fr: to])
        if isinstance(val, str):
            val = val.rstrip('\0')
        metadata[key] = val

    return metadata


def decode_image_to_bytes(image: Union[Iterable[np.uint8], Image.Image]
                          ) -> (bytes, Metadata):
    data = bytes(list(np.asarray(image, dtype=np.uint8).flatten()))
    metadata = parse_metadata(data)
    sign = metadata['sign']
    if sign:
        print(f'This image has been signed: {sign}')
    file_data_hex = ''.join(
        f'{pixel:0>2x}' for pixel in data[metadata['metadata_size']:]
    )
    file_bytes = bytes.fromhex(
        file_data_hex[:len(file_data_hex) - metadata['extra_bytes'] * 2]
    )
    return file_bytes, metadata


def decode_image_name(input_file_path: str, output_file_path: str):
    try:
        if not input_file_path.endswith('.png'):
            input_file_path += '.png'
        image = Image.open(input_file_path)
    except OSError:
        print('Invalid file.')
        return
    file_bytes, metadata = decode_image_to_bytes(image)
    with open(f'{output_file_path}/{metadata["file_name"]}', 'wb') as f:
        f.write(file_bytes)


def int_to_bytes(num: int, num_bytes: int, signed: bool = False) -> bytes:
    return num.to_bytes(num_bytes, byteorder='big', signed=signed)


def bytes_to_int(bytes_: bytes, signed: bool = False) -> int:
    return int.from_bytes(bytes_, 'big', signed=signed)


def str_to_bytes(string: str, num_bytes: int = 0) -> bytes:
    return string.encode()[:num_bytes].ljust(num_bytes, b'\0')


def bytes_to_str(bytes_: bytes) -> str:
    return bytes_.decode()


def bytes_to_hex(bytes_: bytes) -> List[str]:
    return list(map(lambda b: f'{b:02x}', bytes_))


def int_to_n_hex(num: int, num_hex: int) -> List[str]:
    return bytes_to_hex(int_to_bytes(num, num_hex))


def str_to_hex(string: str, num_hex: int = 0) -> List[str]:
    return bytes_to_hex(str_to_bytes(string, num_hex))


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


def hex_bytes_to_colors(hex_bytes: List[str]) -> List[str]:
    colors = []
    color = '#'
    for byte_hex in hex_bytes:
        color += byte_hex
        if len(color) == 7:
            colors.append(color)
            color = '#'
    if color != '#':
        while len(color) < 7:
            color += '0'
        colors.append(color)
    return colors


def encode_bytes_to_colors(input_file_bytes: bytes, file_name: str,
                           sign: str = '') -> List[str]:
    input_file_hex = bytes_to_hex(input_file_bytes)
    extra_bytes = -len(input_file_hex) % 3
    metadata_hex = [
        *int_to_n_hex(extra_bytes, 1),
        *str_to_hex(sign, 50),
        *str_to_hex(file_name, 256)
    ]
    metadata_hex += int_to_n_hex(0, -len(metadata_hex) % 3)
    metadata_hex = int_to_n_hex(len(metadata_hex) + 3, 3) + metadata_hex
    return hex_bytes_to_colors(metadata_hex + input_file_hex)


def encode_bytes_to_image(input_file_bytes: bytes, file_name: str,
                          sign: str = '') -> Image.Image:
    colors = encode_bytes_to_colors(input_file_bytes, file_name, sign)
    return colors_to_image(colors)


def get_file_bytes(input_file_path: str) -> Optional[bytes]:
    try:
        with open(input_file_path, 'rb') as f:
            return f.read()
    except OSError:
        return None


def encode_file_name(input_file_path: str, output_file_path: str,
                     sign: str = ''):
    input_file_bytes = get_file_bytes(input_file_path)
    if input_file_bytes is None:
        print('Invalid file.')
        return
    file_name = os.path.basename(input_file_path)
    colors = encode_bytes_to_colors(input_file_bytes, file_name, sign)
    image = colors_to_image(colors)
    image.save(f'{output_file_path}/{file_name}.png')


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
        help='output folder',
        default='.'
    )
    parser.add_argument(
        '-s', '--sign',
        type=str,
        help='sign the encoded image (max 50 characters)',
        default=''
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
        input_file_path = input(
            'Enter the input filepath of the file to encode: '
        )
    else:
        input_file_path = input(
            'Enter the input filename of the image to decode: '
        )

    output_file_path = input('Enter the output path (ENTER for .): ') or '.'

    if mode == 'e':
        sign = input(
            'Sign the encoded image (max 50 characters, ENTER for blank): '
        )
    else:
        sign = ''

    return {
        'mode': mode,
        'input': input_file_path,
        'output': output_file_path,
        'sign': sign
    }


def process_args() -> Dict[str, str]:
    if not len(sys.argv) > 1:
        return process_args_interactive()
    args = parse_args()
    return {
        'mode': 'd' if args.decode else 'e',
        'input': args.input,
        'output': args.output,
        'sign': args.sign
    }


def main():
    args = process_args()
    if args['mode'] == 'e':
        encode_file_name(args['input'], args['output'], args['sign'])
    elif args['mode'] == 'd':
        decode_image_name(args['input'], args['output'])


if __name__ == '__main__':
    main()
