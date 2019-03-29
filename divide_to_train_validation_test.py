import os
import random
import shutil

def walk(path, callback):
    for fpath, _, file_list in os.walk(path):
        for file_name in file_list:
            path = os.path.join(fpath, file_name)
            callback(path)


def divide_to_train_validation_test(from_dir, train_dir, validation_dir, test_dir):
    """
    取 1/8 的数据
    训练集，验证集，测试集 6:2:2
    """
    def move(path):
        n1 = random.randint(0, 7)
        if n1 == 0:
            (_, tempfilename) = os.path.split(path)
            n2 = random.randint(0, 9)
            if n2 >= 0 and n2 <= 5:
                new_path = os.path.join(train_dir, tempfilename)
            elif n2 >= 6 and n2 <= 7:
                new_path = os.path.join(validation_dir, tempfilename)
            else:
                new_path = os.path.join(test_dir, tempfilename)
            print('copy:', new_path)
            shutil.copyfile(path, new_path)
    walk(from_dir, move)


def os_path_join_and_mk(father, dirname):
    new_path = os.path.join(father, dirname)
    if not os.path.exists(new_path):
        os.mkdir(new_path)
    return new_path


random.seed(2017)

image_size = 299
current_dir = os.path.dirname(__file__)
base_dir = os.path.join(current_dir, 'base' + '_' + str(image_size))
first_scan_base = os.path.join(base_dir, 'first-scan')
second_scan_base = os.path.join(base_dir, 'second-scan')

dataset_dir = os_path_join_and_mk(current_dir, 'dataset')
train_dir = os_path_join_and_mk(dataset_dir, 'train')
validation_dir = os_path_join_and_mk(dataset_dir, 'validation')
test_dir = os_path_join_and_mk(dataset_dir, 'test')

first_scan_train_dataset = os_path_join_and_mk(train_dir, 'first-scan')
second_scan_train_dataset = os_path_join_and_mk(train_dir, 'second-scan')
first_scan_validation_dataset = os_path_join_and_mk(
    validation_dir, 'first-scan')
second_scan_validation_dataset = os_path_join_and_mk(
    validation_dir, 'second-scan')
first_scan_test_dataset = os_path_join_and_mk(
    test_dir, 'first-scan')
second_scan_test_dataset = os_path_join_and_mk(
    test_dir, 'second-scan')

divide_to_train_validation_test(first_scan_base, first_scan_train_dataset,
                                first_scan_validation_dataset, first_scan_test_dataset)
divide_to_train_validation_test(second_scan_base, second_scan_train_dataset,
                                second_scan_validation_dataset, second_scan_test_dataset)
