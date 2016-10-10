import os
import argparse

from PIL import Image


def exit_if_errors(args):
    if args.scale is not None and (args.width is not None or args.height is not None):
        print('You can not specify both the width, height and scale.')
        exit(1)
    if args.scale is not None and args.width is not None and args.height is not None:
        print('You must specify the size of the output image.')
        exit(1)
    if not os.path.exists(args.path):
        print('Image does not exists.')
        exit(1)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='path to the image')
    parser.add_argument('--width', type=int)
    parser.add_argument('--height', type=int)
    parser.add_argument('--scale', type=float)
    parser.add_argument('--output')
    return parser.parse_args()


def resize_image(path, **kwargs):
    img = Image.open(path)

    scale = kwargs['scale']
    if scale is not None:
        size = int(img.width * scale), int(img.height * scale)
        return img.resize(size, Image.ANTIALIAS)

    width, height = kwargs['width'], kwargs['height']
    if height is None:
        scale = width / img.width
        size = width, int(img.height * scale)
        return img.resize(size, Image.ANTIALIAS)

    if width is None:
        scale = height / img.height
        size = int(img.width * scale), height
        return img.resize(size, Image.ANTIALIAS)

    return img.resize((width, height), Image.ANTIALIAS)


def save_image(image, path_to_result):
    image.save(path_to_result)


def is_proportions_match(path_to_original, image):
    permissible_error = 0.005
    img_original = Image.open(path_to_original)
    proportions = image.width / img_original.width - image.height / img_original.height
    return abs(proportions) < permissible_error


if __name__ == '__main__':
    args = get_args()
    exit_if_errors(args)
    image = resize_image(args.path, scale=args.scale,
                         width=args.width, height=args.height)

    if args.output is not None:
        path_to_result = args.output
    else:
        path = os.path.splitext(os.path.basename(args.path))
        path_to_result = '{}__{}x{}{}'.format(path[0],
                                              str(image.width),
                                              str(image.height),
                                              path[1])
    save_image(image, path_to_result)
    if not is_proportions_match(args.path, image):
        print('The proportions are not same as the original file.')
