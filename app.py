import random
import os
import shutil
from PIL import Image


def wrapper_cut_picture(output_size):
    def cut_picture(path):
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
    return cut_picture


def walk(root_dir, callback):
    for lists in os.listdir(root_dir):
        path = os.path.join(root_dir, lists)
        if os.path.isfile(path) and not os.path.isdir(path):
            callback(path)
        if os.path.isdir(path):
            walk(path, callback)

# sample -> dataset -> base -> train + validation + test


def load_data(path):
    if (os.path.exists(path)):
        return
    else:
        input_dir = './sample'
        output_dir = './dataset'
        output_size = 224
        try:
            shutil.copytree(input_dir, output_dor)
        except FileExistsError:
            print('file exists')

        callback = wrapper_cut_picture(output_size)
        walk(output_dir, callback)


current_path = os.path.dirname(__file__)
dataset_dir = './dataset'
load_data(dataset_dir)


def mkdir_if_not_exists(dirname):
    if not os.path.exists(dirname):
        os.mkdir(dirname)


base_dir = os.path.join(current_path, 'base')
mkdir_if_not_exists(base_dir)

train_dir = os.path.join(base_dir, 'train')
mkdir_if_not_exists(train_dir)
validation_dir = os.path.join(base_dir, 'validation')
mkdir_if_not_exists(validation_dir)
test_dir = os.path.join(base_dir, 'test')
mkdir_if_not_exists(test_dir)

train_first_scan_dir = os.path.join(train_dir, 'first-scan')
validation_first_scan_dir = os.path.join(validation_dir, 'first-scan')
test_first_scan_dir = os.path.join(test_dir, 'first-scan')

train_second_scan_dir = os.path.join(train_dir, 'second-scan')
validation_second_scan_dir = os.path.join(validation_dir, 'second-scan')
test_second_scan_dir = os.path.join(test_dir, 'second-scan')

# 将 first-scan 的图片随机复制到 train, validation, test 的文件夹中
# 数据集万级别，按比例 6 ： 2 ： 2 划分
first_scan_dataset_dir = os.path.join(dataset_dir, 'first-scan')
second_scan_dataset_dir = os.path.join(dataset_dir, 'second-scan')


def first_scan_to_target(path):
    flag = random.randint(0, 9)
    if flag >= 0 and flag <= 5:
        shutil.copyfile(path, train_first_scan_dir)
    else if flag >= 6 and flag <= 7:
        shutil.copyfile(path, validation_first_scan_dir)
    else:
        shutil.copyfile(path, test_first_scan_dir)


def second_scan_to_target(path):
    flag = random.randint(0, 9)
    if flag >= 0 and flag <= 5:
        shutil.copyfile(path, train_second_scan_dir)
    else if flag >= 6 and flag <= 7:
        shutil.copyfile(path, validation_second_scan_dir)
    else:
        shutil.copyfile(path, test_second_scan_dir)


walk(first_scan_dataset_dir, first_scan_to_target)
walk(second_scan_dataset_dir, second_scan_to_target)


def print_num_of_dataset():
    print('total training first scan images:',
          len(os.listdir(train_first_scan_dir)))
    print('total validation first scan images:',
          len(os.listdir(validation_first_scan_dir)))
    print('total test first scan images:',
          len(os.listdir(test_first_scan_dir)))
    print('total training second scan images:',
          len(os.listdir(train_second_scan_dir)))
    print('total validation second scan images:',
          len(os.listdir(validation_second_scan_dir)))
    print('total test second scan images:',
          len(os.listdir(test_second_scan_dir)))


print_num_of_dataset()
