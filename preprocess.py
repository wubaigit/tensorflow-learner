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
                output_img_name = os.path.join(
                    output_dir, '%s_%s%s' % (filename, i, extension))
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


def copy_image(father_path, path, times):
    (filename, extension) = os.path.splitext(path)

    for i in range(0, times):
        new_filename = filename + '_' + str(i) + extension
        new_file_path = os.path.join(father_path, new_filename)
        shutil.copyfile(path, new_file_path)


def oversampling(sample1_dir, sample2_dir):
    """一次扫描的数据会远远小于二次扫描的，
        这里采用 过采样 的方式
    """
    sample1_content = os.listdir(sample1_dir)
    sample2_content = os.listdir(sample2_dir)
    sample1_content_len = len(sample1_content)
    sample2_content_len = len(sample2_content)

    if sample1_content_len > sample2_content_len:
        times = int(sample1_content_len / sample2_content_len)
        if times >= 2:
            for fname in sample1_content:
                path = os.path.join(sample1_dir, fname)
                copy_image(sample1_dir, path, times - 1)
    else:
        times = int(sample2_content_len / sample1_content_len)
        if times >= 2:
            for fname in sample2_content:
                path = os.path.join(sample2_dir, fname)
                copy_image(sample2_dir, path, times - 1)


def load_data(output_size):
    current_path = os.path.dirname(__file__)

    sample_dir = os.path.join(current_path, 'sample')
    first_scan_sample = os.path.join(sample_dir, 'first-scan')
    second_scan_sample = os.path.join(sample_dir, 'second-scan')

    base_dir = os.path.join(current_path, 'base')
    mkdir_if_not_exists(base_dir)

    def generate_base_sample(sample_size):
        sample_size_dir = os.path.join(base_dir, sample_size)
        mkdir_if_not_exists(sample_size_dir)
        first_scan_base = os.path.join(sample_size_dir, 'first-scan')
        mkdir_if_not_exists(first_scan_base)
        second_scan_base = os.path.join(sample_size_dir, 'second-scan')
        mkdir_if_not_exists(second_scan_base)
        return (first_scan_base, second_scan_base)

    (first_scan_base, second_scan_base) = generate_base_sample(str(output_size))
    if len(os.listdir(first_scan_base)) == 0:
        walk(first_scan_sample, wrapper_cut_picture(
            output_size, first_scan_base))
        print(first_scan_base, 'over')
    if len(os.listdir(second_scan_base)) == 0:
        walk(second_scan_sample, wrapper_cut_picture(
            output_size, second_scan_base))
        print(second_scan_base, 'over')

    oversampling(first_scan_base, second_scan_base)

    train_dir = os.path.join(base_dir, 'train')
    os.mkdir(train_dir)
    validation_dir = os.path.join(base_dir, 'validation')
    os.mkdir(validation_dir)
    test_dir = os.path.join(base_dir, 'test')
    os.mkdir(test_dir)

    def mkdir_dir(father_dir, dirname):
        new_dir = os.path.join(father_dir, dirname)
        mkdir_if_not_exists(new_dir)
        return new_dir

    train_first_scan_dir = mkdir_dir(train_dir, 'first-scan')
    train_second_scan_dir = mkdir_dir(train_dir, 'second-scan')

    validation_first_scan_dir = mkdir_dir(validation_dir, 'first-scan')
    validation_second_scan_dir = mkdir_dir(validation_dir, 'second-scan')

    test_first_scan_dir = mkdir_dir(test_dir, 'first-scan')
    test_second_scan_dir = mkdir_dir(test_dir, 'second-scan')


# load_data(224)
load_data(299)

# first_scan_224 = './base/224/first-scan'
# second_scan_224 = './base/224/second-scan'
first_scan_299 = './base/299/first-scan'
second_scan_299 = './base/299/second-scan'


# def print_len_listdir(dirname):
#     print(len(os.listdir(dirname)))

# print_len_listdir(first_scan_224)   # 87168
# print_len_listdir(second_scan_224)  # 436150
# print_len_listdir(first_scan_299)   # 48444
# print_len_listdir(second_scan_299)  # 242450

first_scan_299_len = len(os.listdir(first_scan_299))
second_scan_299_len = len(os.listdir(second_scan_299))

times = second_scan_299_len / first_scan_299_len
