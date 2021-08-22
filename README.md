# Imaginenc

Converts any file into an image, and images back to files.
Currently, there is no built-in way of knowing the file type of the converted image.  
Linux users can use the `file` command.  
Windows doesn't have anything by default, so users would need to download a Terminal Emulator.  

![Source Code Image](images/imaginenc.py.png "Source Code Image")

## Installation and usage

Install [Python 3.8+](https://www.python.org/) and add it to the system path.  
Run `pip install -r requirements.txt` inside the folder and wait for the installation to finish.  
Run `python imaginenc.py`

```
usage: imaginenc.py [-h] (-e | -d) -i INPUT -o OUTPUT

Converts any file into an image, and images back to files. Run without args for interactive input mode.

optional arguments:
  -h, --help            show this help message and exit
  -e, --encode          encode file to image
  -d, --decode          decode image to file
  -i INPUT, --input INPUT
                        input file
  -o OUTPUT, --output OUTPUT
                        output file
```

## Planned Features

- More intuitive usage.
- File type detection (for decoding images).
- Better encryption.
