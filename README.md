# Imaginenc

[![PyPI](https://img.shields.io/pypi/v/imaginenc)](https://pypi.python.org/pypi/imaginenc)
[![Versions](https://img.shields.io/pypi/pyversions/imaginenc)](https://pypi.python.org/pypi/imaginenc)
[![License](https://img.shields.io/pypi/l/imaginenc)](https://pypi.python.org/pypi/imaginenc)
[![Build](https://img.shields.io/github/workflow/status/LordDeatHunter/Imaginenc/Python%20application)]()


Convert any file into an image, and images back to files.  

![Source Code Image](https://raw.githubusercontent.com/LordDeatHunter/Imaginenc/master/images/imaginenc.py.png "Source Code Image")

## Installation

Imaginenc is available on PyPI:
```console
$ python -m pip install imaginenc
```
Imaginenc requires Python 3.8+. 

## Usage

```console
usage: imaginenc [-h] (-e | -d) -i INPUT [-o OUTPUT] [-s SIGN]

Convert any file into an image, and images back to files. Run without args for interactive input mode.

optional arguments:
  -h, --help            show this help message and exit
  -e, --encode          encode file to image
  -d, --decode          decode image to file
  -i INPUT, --input INPUT
                        input file
  -o OUTPUT, --output OUTPUT
                        output folder
  -s SIGN, --sign SIGN  sign the encoded image (max 50 characters)
```

## Examples of imaginenc command

Encode

```bash
imaginenc -e -i imaginenc\imaginenc.py -o images -s "Thank you for using this tool!"
```

Decode

```bash
imaginenc -d -i images\imaginenc.py.png -o output
```

## Examples of imaginenc module

Import

```python
import imaginenc
```

Encode file name and save as image

```python
imaginenc.encode_file_name(
    input_file_path='imaginenc/imaginenc.py',
    output_file_path='images',
    sign='signature'
)
```

Encode file bytes and return image

```python
with open('imaginenc/imaginenc.py') as f:
    image = imaginenc.encode_bytes_to_image(
        input_file_bytes=f.read(),
        file_name=f.name(),
        sign='signature'
    )
```

Decode image name and save as original file

```python
metadata = imaginenc.decode_image_name(
    input_file_path='images/imaginenc.py.png',
    output_file_path='output'
)
```

Decode PIL image to original file bytes

```python
from PIL import Image

image = Image.open('images/imaginenc.py.png')
file_bytes, metadata = imaginenc.decode_image_to_bytes(
    image=image
)
```

## Planned Features

- Encryption.
