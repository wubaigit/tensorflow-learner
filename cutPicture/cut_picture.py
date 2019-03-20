import os
import shutil
from PIL import Image


def cut_picture(path, output_size):
    (filepath, tempfilename) = os.path.split(path)
    (filename, extension) = os.path.splitext(tempfilename)

    current_path = os.path.dirname(path)
    print(filepath)

    img = Image.open(path)
    width = img.size[0]
    height = img.size[1]

    y_position = 0
    i = 0
    while True:
        if y_position + output_size > height:
            break
        x_position = 0
        while True:
            if x_position + output_size > width:
                break
            left = x_position
            top = y_position
            right = x_position + output_size
            bottom = y_position + output_size
            output_img = img.crop((left, top, right, bottom))
            output_img.save(os.path.join(
                current_path, './%s-%s.%s' % (filename, i, extension)))
            x_position += output_size
            i += 1
        y_position += output_size
    os.remove(path)


def walk(output_dir, output_size):
    for lists in os.listdir(output_dir):
        path = os.path.join(output_dir, lists)
        if os.path.isfile(path) and not os.path.isdir(path):
            cut_picture(path, output_size)
        if os.path.isdir(path):
            walk(path, output_size)


input_dir = './input'
output_dir = './output'


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 4:
        input_dir = sys.argv[1]
        output_dir = sys.argv[2]
        output_size = int(sys.argv[3])
        print(output_size)

        try:
            shutil.copytree(input_dir, output_dir)
        except FileExistsError:
            print('file exists')

        walk(output_dir, output_size)
    else:
        print('argv is less then four')
