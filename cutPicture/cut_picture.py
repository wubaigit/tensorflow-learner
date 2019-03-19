import os
from PIL import Image


def cut_picture(path, output_dir):
    (filepath, tempfilename) = os.path.split(path)
    (filename, extension) = os.path.splitext(tempfilename)
    img = Image.open(path)
    width = img.size[0]
    height = img.size[1]

    y_position = 0
    i = 0
    while True:
        if y_position + 224 > height:
            break
        x_position = 0
        while True:
            if x_position + 224 > width:
                break
            left = x_position
            top = y_position
            right = x_position + 224
            bottom = y_position + 224
            output_img = img.crop((left, top, right, bottom))
            output_img.save(os.path.join(
                output_dir, './%s-%s.%s' % (filename, i, extension)))
            x_position += 224
            i += 1
        y_position += 224


def walk(input_dir, output_dir):
    for lists in os.listdir(input_dir):
        path = os.path.join(input_dir, lists)
        if os.path.isfile(path) and not os.path.isdir(path):
            cut_picture(path, output_dir)
        if os.path.isdir(path):
            walk(path, output_dir)

input_dir = './input'
output_dir = './output'
walk(input_dir, output_dir)