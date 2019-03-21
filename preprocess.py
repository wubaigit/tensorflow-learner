import os
import shutil
from PIL import Image

Image.MAX_IMAGE_PIXELS = 1000000000

def mkdir_if_not_exists(dirname):
    if not os.path.exists(dirname):
        os.mkdir(dirname)

def wrapper_cut_picture(output_size, output_dir):
    def cut_picture(path):
        (_, tempfilename) = os.path.split(path)
        (filename, extension) = os.path.splitext(tempfilename)
        print('input:', path)

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
                output_img_name = os.path.join(output_dir, '%s_%s%s'%(filename, i, extension))
                print('output:', output_img_name)
                output_img.save(output_img_name)
                x_position += output_size
                i += 1
            y_position += output_size
    return cut_picture

def walk(root_dir, callback):
    for fname in os.listdir(root_dir):
        path = os.path.join(root_dir, fname)
        if os.path.isfile(path) and not os.path.isdir(path):
            callback(path)
        if os.path.isdir(path):
            walk(path, callback)

def load_data(output_size):
    current_path = os.path.dirname(__file__)
    
    sample_dir = os.path.join(current_path, 'sample')
    first_scan_sample = os.path.join(sample_dir, 'first-scan')
    second_scan_sample = os.path.join(sample_dir, 'second-scan')

    base_dir = os.path.join(current_path, 'base')
    mkdir_if_not_exists(base_dir)
    def sample(sample_size):
        sample_size_dir = os.path.join(base_dir, sample_size)
        mkdir_if_not_exists(sample_size_dir)
        first_scan_base = os.path.join(sample_size_dir, 'first-scan')
        mkdir_if_not_exists(first_scan_base)
        second_scan_base = os.path.join(sample_size_dir, 'second-scan')
        mkdir_if_not_exists(second_scan_base)
        return (first_scan_base, second_scan_base)    

    (first_scan_base, second_scan_base) = sample(str(output_size))
    if len(os.listdir(first_scan_base)) != 0 and len(os.listdir(second_scan_base)) != 0:
        return
    walk(first_scan_sample, wrapper_cut_picture(output_size, first_scan_base))
    walk(second_scan_sample, wrapper_cut_picture(output_size, second_scan_base))


load_data(224)
load_data(299)

first_scan_224 = './base/224/first-scan'
second_scan_224 = './base/224/second-scan'
first_scan_299 = './base/299/first-scan'
second_scan_299 = './base/299/second-scan'


def print_len_listdir(dirname):
    print(len(os.listdir(dirname)))

print_len_listdir(first_scan_224)   # 87168
print_len_listdir(second_scan_224)  # 436150
print_len_listdir(first_scan_299)   # 48444
print_len_listdir(second_scan_299)  # 242450