import os
import argparse

from PIL import Image


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='path to the image')
    parser.add_argument('--width', type=int)
    parser.add_argument('--height', type=int)
    parser.add_argument('--scale', type=float)
    parser.add_argument('--output')
    return parser.parse_args()


def open_image(path):
    return Image.open(path)


def save_image(image, path_to_result):
    image.save(path_to_result)


def validate_arguments_for_image_size(width, height, scale):
    if scale is not None and (width is not None or height is not None):
        raise ValueError('You can not specify both the width, height and scale.')
    if scale is None and width is None and height is None:
        raise ValueError('You must specify the size of the output image.')


def get_new_image_size(width, height, scale):
    validate_arguments_for_image_size(width, height, scale)

    if scale is not None:
        return int(image.width * scale), int(image.height * scale)

    if height is None:
        scale = width / image.width
        return width, int(image.height * scale)

    if width is None:
        scale = height / image.height
        return int(image.width * scale), height


def resize_image(image, width=None, height=None, scale=None):
    validate_arguments_for_image_size(width, height, scale)
    size = get_new_image_size(width, height, scale)
    return image.resize(size, Image.ANTIALIAS)


def is_proportions_match(image, width, height, scale):
    validate_arguments_for_image_size(width, height, scale)
    permissible_error = 0.005
    new_width, new_height = get_new_image_size(width, height, scale)
    proportions = new_width / image.width - new_height / image.height
    return abs(proportions) < permissible_error


def parse_output_path_for_new_image(output_path, path_to_image, image):
    if output_path is not None:
        return output_path
    else:
        filename, file_ext = os.path.splitext(os.path.basename(path_to_image))
        return '{}__{}x{}{}'.format(filename,
                                    image.width,
                                    image.height,
                                    file_ext)


if __name__ == '__main__':
    args = get_args()
    if not os.path.exists(args.path):
        print('Image does not exists.')
        exit(1)
    image = open_image(args.path)
    try:
        if not is_proportions_match(image, scale=args.scale,
                                    width=args.width, height=args.height):
            print('The proportions are not same as the original file.')
        new_image = resize_image(image, scale=args.scale,
                                 width=args.width, height=args.height)
    except ValueError as err:
        print(str(err))
        exit(1)

    path_to_result = parse_output_path_for_new_image(args.output, args.path, new_image)
    save_image(new_image, path_to_result)
