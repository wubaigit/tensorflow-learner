import os
import shutil
import random

current_dir = os.path.dirname(__file__)

def walk(path, callback):
    for fpath, _, file_list in os.walk(path):
        for file_name in file_list:
            cu_path = os.path.join(fpath, file_name)
            callback(cu_path)

def move_one_eighth(from_dir, to_dir):
    def move(path):
        (_, tempfilename) = os.path.split(path)
        num = random.randint(0, 7)
        if num == 1:
            new_path = os.path.join(to_dir, tempfilename)
            print('add:', new_path)
            shutil.copyfile(path, new_path)
    walk(from_dir, move)

def os_path_join_and_mkdir(father_dir, dirname):
    new_path = os.path.join(father_dir, dirname)
    if not os.path.exists(new_path):
        os.mkdir(new_path)
    return new_path

dataset_299 = os.path.join(current_dir, 'dataset_299')
train_dir = os.path.join(dataset_299, 'train')
validation_dir = os.path.join(dataset_299, 'validation')
train_dir_first_scan = os.path.join(train_dir, 'first-scan')
train_dir_second_scan = os.path.join(train_dir, 'second-scan')
validation_dir_first_scan = os.path.join(validation_dir, 'first-scan')
validation_dir_second_scan = os.path.join(validation_dir, 'second-scan')


dataset_299_one_eighth = os_path_join_and_mkdir(current_dir, 'dataset_299_one_eighth')

train_dir_one_eighth = os_path_join_and_mkdir(dataset_299_one_eighth, 'train')
train_dir_one_eighth_first_scan = os_path_join_and_mkdir(train_dir_one_eighth, 'first-scan')
train_dir_one_eighth_second_scan = os_path_join_and_mkdir(train_dir_one_eighth, 'second-scan')

validation_dir_one_eighth = os_path_join_and_mkdir(dataset_299_one_eighth, 'validation')
validation_dir_one_eighth_first_scan = os_path_join_and_mkdir(validation_dir_one_eighth, 'first-scan')
validation_dir_one_eighth_second_scan = os_path_join_and_mkdir(validation_dir_one_eighth, 'second-scan')

move_one_eighth(train_dir_first_scan, train_dir_one_eighth_first_scan)
move_one_eighth(train_dir_second_scan, train_dir_one_eighth_second_scan)
move_one_eighth(validation_dir_first_scan, validation_dir_one_eighth_first_scan)
move_one_eighth(validation_dir_second_scan, validation_dir_one_eighth_second_scan)