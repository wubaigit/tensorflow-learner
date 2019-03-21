import os
import shutil
import re

current_father_dir = os.path.dirname(__file__)

def walk(root_dir, callback):
    for fname in os.listdir(root_dir):
        path = os.path.join(root_dir, fname)
        if os.path.isfile(path) and not os.path.isdir(path):
            callback(path)
        if os.path.isdir(path):
            walk(path, callback)

def move_file(path, target):
   shutil.move(path, target)

def callback(path):
    if path == __file__:
        return
    new_dir_arr = re.findall(r'\\(.+?)\\(.+?)\\(.+?)\\', path)[0]
    new_dir = os.path.join(current_father_dir, new_dir_arr[0] + '_' + new_dir_arr[1] + '_' + new_dir_arr[2])
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
    move_file(path, new_dir)

for fname in os.listdir(current_father_dir):
    path = os.path.join(current_father_dir, fname)
    walk(path, callback)
