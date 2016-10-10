12_image_resize
===============

This script changes the input image size according to the input
parameters.

Usage
-----

```
~$ pip install -r requirements.txt
~$ python3 image_resize.py -h
usage: image_resize.py [-h] [--width WIDTH] [--height HEIGHT] 
[--scale SCALE] [--output OUTPUT] path
positional arguments:
  path             path to the image

optional arguments:
  -h, --help       show this help message and exit
  --width WIDTH
  --height HEIGHT
  --scale SCALE
  --output OUTPUT
~$ python3 image_resize.py cat.png --scale 2
```

Requirements
------------

- Python >= 3.5
- Pillow==3.3.0
