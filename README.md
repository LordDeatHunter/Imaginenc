# Imaginenc

Convert any file into an image, and images back to files. Currently, there is
no built-in way of knowing the file type of the converted image.  
Linux users can use the `file` command.  
Windows doesn't have anything by default, so users would need to download a
Terminal Emulator.

![Source Code Image](https://raw.githubusercontent.com/LordDeatHunter/Imaginenc/master/images/imaginenc.py.png "Source Code Image")

## Installation

Install [Python 3.8+](https://www.python.org/) and add it to the system path.  
Run `pip install -r requirements.txt` inside the folder and wait for the
installation to finish.  
Run `python imaginenc.py`

## Usage

```
usage: imaginenc.py [-h] (-e | -d) -i INPUT [-o OUTPUT] [-s SIGN]

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
python imaginenc\imaginenc.py -e -i imaginenc\imaginenc.py -o images -s "Thank you for using this tool!"
```

Decode

```bash
python imaginenc\imaginenc.py -d -i images\imaginenc.py.png -o output
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
