"""
准备数据，要输出 train, validation, test 文件夹
阶段一：遍历原数据 sample 文件夹下的文件，将文件裁剪并放到 base 对应的文件夹下 => load_data
阶段二：将 base 文件夹下的数据进行过采样 => oversampling
阶段三：将数据分成 train, validation, test 三类 => divide_to_train_validation_test
"""

import os
import shutil
from PIL import Image

import random

Image.MAX_IMAGE_PIXELS = 1000000000


def os_path_join(father_dir, filename):
    new_file = os.path.join(father_dir, filename)
    if not os.path.exists(new_file):
        os.mkdir(new_file)
    return new_file


def walk(path, callback):
    for fpath, _, file_list in os.walk(path):
        for file_name in file_list:
            path = os.path.join(fpath, file_name)
            callback(path)


def curry_cut_picture(output_image_size, output_dir):
    def cut_picture(path):
        print('input:', path)
        (_, tempfilename) = os.path.split(path)
        (filename, _) = os.path.splitext(tempfilename)

        img = Image.open(path)
        width = img.size[0]
        height = img.size[1]

        y_position = 0
        i = 0
        while True:
            if y_position + output_image_size > height:
                break
            x_position = 0
            while True:
                if x_position + output_image_size > width:
                    break
                left = x_position
                top = y_position
                right = x_position + output_image_size
                bottom = y_position + output_image_size

                output_img = img.crop((left, top, right, bottom))
                output_img_name = os.path.join(
                    output_dir, '%s_%s%s' % (filename, i, '.png'))
                print('output:', output_img_name)
                output_img.save(output_img_name)

                x_position += output_image_size
                i += 1
            y_position += output_image_size
    return cut_picture


def load(root_dir, output_image_size, output_dir):
    walk(root_dir, curry_cut_picture(output_image_size, output_dir))


def copy_image(path, times):
    father_dir = os.path.dirname(path)
    (_, tempfilename) = os.path.split(path)
    (filename, extension) = os.path.splitext(tempfilename)

    for i in range(0, times):
        new_filename = filename + '_' + str(i) + extension
        new_file_path = os.path.join(father_dir, new_filename)
        shutil.copyfile(path, new_file_path)


def oversampling(sample1_dir, sample2_dir):
    sample1_content = os.listdir(sample1_dir)
    sample2_content = os.listdir(sample2_dir)
    sample1_content_len = len(sample1_content)
    sample2_content_len = len(sample2_content)

    if sample1_content_len > sample2_content_len:
        times = int(sample1_content_len / sample2_content_len)
        if times >= 2:
            for fname in sample2_content:
                path = os_path_join(sample2_dir, fname)
                copy_image(path, times - 1)
    else:
        times = int(sample2_content_len / sample1_content_len)
        if times >= 2:
            for fname in sample1_content:
                path = os_path_join(sample1_dir, fname)
                copy_image(path, times - 1)


def divide_to_train_validation_test(from_dir, train_dir, validation_dir, test_dir):
    """
    训练集，验证集，测试集 划分比例暂不明确
    """
    def move(path):
        (_, tempfilename) = os.path.split(path)
        num = random.randint(0, 9)
        if num >= 0 and num <= 7:
            new_path = os.path.join(train_dir, tempfilename)
        elif num == 8:
            new_path = os.path.join(validation_dir, tempfilename)
        else:
            new_path = os.path.join(test_dir, tempfilename)
        shutil.copyfile(path, new_path)
    walk(from_dir, move)


def load_data(image_size):
    current_dir = os.path.dirname(__file__)

    sample_dir = os_path_join(current_dir, 'sample')
    first_scan_sample = os_path_join(sample_dir, 'first-scan')
    second_scan_sample = os_path_join(sample_dir, 'second-scan')

    base_dir = os_path_join(current_dir, 'base' + '_' + str(image_size))
    first_scan_base = os_path_join(base_dir, 'first-scan')
    second_scan_base = os_path_join(base_dir, 'second-scan')

    load(first_scan_sample, image_size, first_scan_base)
    load(second_scan_sample, image_size, second_scan_base)

    oversampling(first_scan_base, second_scan_base)

    dataset_dir = os.path.join(current_dir, 'dataset' + '_' + str(image_size))
    train_dir = os.path.join(dataset_dir, 'train')
    validation_dir = os.path.join(dataset_dir, 'validation')
    test_dir = os.path.join(dataset_dir, 'test')

    if not os.path.exists(dataset_dir):
        os.mkdir(dataset_dir)
        os.mkdir(train_dir)
        os.mkdir(validation_dir)
        os.mkdir(test_dir)

        first_scan_dataset_train = os_path_join(train_dir, 'first-scan')
        first_scan_dataset_validation = os_path_join(
            validation_dir, 'first-scan')
        first_scan_dataset_test = os_path_join(test_dir, 'first-scan')

        second_scan_dataset_train = os_path_join(train_dir, 'second-scan')
        second_scan_dataset_validation = os_path_join(
            validation_dir, 'second-scan')
        second_scan_dataset_test = os_path_join(test_dir, 'second-scan')

        divide_to_train_validation_test(
            first_scan_base, first_scan_dataset_train, first_scan_dataset_validation, first_scan_dataset_test)
        divide_to_train_validation_test(second_scan_base, second_scan_dataset_train,
                                        second_scan_dataset_validation, second_scan_dataset_test)

    return (dataset_dir, train_dir, validation_dir, test_dir)

if __name__ == "__main__":
    # load_data(224)
    load_data(299)